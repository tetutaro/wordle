"use strint";
const os = require("os");
const {app, BrowserWindow} = require("electron");
const path = require("path");
const reqp = require("request-promise-native");

let mainWindow = null;
let subpy = null;

const url = 'http://localhost:8000/';
/*
 * if you use "backend_onefile.spec" in PyInstaller (make backend),
 * BACKEND_EXE_FILE = path.join(
 *  __dirname, "backend_dist/wordle_backend"
 * );
 */
const BACKEND_EXE_FILE = path.join(
    __dirname, "backend_dist/wordle_backend/wordle_backend"
);

function sleep(msec) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + msec);
}

const startPythonSubprocess = () => {
    if (require("fs").existsSync(BACKEND_EXE_FILE)) {
        subpy = require("child_process").execFile(BACKEND_EXE_FILE, []);
    } else {
        subpy = require("child_process").spawn(
            "python", ["-m", "backend"]
        );
    }
};

const killPythonSubprocesses = (main_pid) => {
    let useBinary = false;
    if (require("fs").existsSync(BACKEND_EXE_FILE)) {
        useBinary = true;
    }
    let cleanupCompleted = false;
    require("ps-tree")(main_pid, (err, children) => {
        children.forEach((x) => {
            if (os.platform() == "darwin") {
                if (useBinary) {
                    if (x.COMM == BACKEND_EXE_FILE) {
                        process.kill(x.PID);
                    }
                } else {
                    if (x.COMM.endsWith("bin/python")) {
                        process.kill(x.PID);
                    }
                }
            } else if (os.platform() == "linux") {
                if (useBinary) {
                    if (x.COMMAND == "wordle_backend") {
                        process.kill(x.PID);
                    }
                } else {
                    if (x.COMMAND == "python") {
                        process.kill(x.PID);
                    }
                }
            }
        });
        subpy = null;
        cleanupCompleted = true;
    });
    return new Promise(function (resolve, reject) {
        (function waitForSubProcessCleanup() {
            if (cleanupCompleted) return resolve();
            setTimeout(waitForSubProcessCleanup, 30);
        })();
    });
};

let sleep_count = 0;

const createMainWindow = () => {
    mainWindow = new BrowserWindow({
        width: 510,
        height: 720,
        resizable: false,
        webPreferences: {
            nodeIntegration: false
        }
    });
    mainWindow.setMenuBarVisibility(false);
    mainWindow.loadURL(url);
    mainWindow.on("closed", () => {
        mainWindow = null;
    });
    mainWindow.webContents.on("did-fail-load", function() {
        if (!require("fs").existsSync(BACKEND_EXE_FILE)) {
            console.log('%s not exitst', BACKEND_EXE_FILE);
        }
        if (subpy == null) {
            console.log('backend is not running. restart.');
            startPythonSubprocess();
        }
        sleep_count += 1;
        console.log('fail to access Wordle (%d)...', sleep_count);
        sleep(1000);
        mainWindow.loadURL(url);
    });
};

app.on("ready", function () {
    startPythonSubprocess();
    var startUp = function() {
        reqp(url)
            .then((html) => {
                console.log("Let's Wordle");
                createMainWindow();
            })
            .catch((err) => {
                if (!require("fs").existsSync(BACKEND_EXE_FILE)) {
                    console.log('%s not exitst', BACKEND_EXE_FILE);
                }
                if (subpy == null) {
                    console.log('backend is not running. restart.');
                    startPythonSubprocess();
                }
                sleep_count += 1;
                console.log(
                    'waiting for starting Wordle (%d)...', sleep_count
                );
                sleep(1000);
                startUp();
            });
    };
    startUp();
});

app.on('activate', function () {
    if (subpy == null) {
        startPythonSubprocess();
    }
    if (mainWindow === null) {
        createMainWindow();
    }
});

app.on('window-all-closed', function () {
    killPythonSubprocesses(process.pid).then(() => {
        app.quit();
    });
});
