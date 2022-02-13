"use strint";
const {app, BrowserWindow} = require('electron');
const path = require('path');

let mainWindow = null;
let subpy = null;

const BACKEND_EXE_FILE = path.join(__dirname, "backend_dist/backend");

const startPythonSubprocess = () => {
    if (require("fs").existsSync(BACKEND_EXE_FILE)) {
        subpy = require("child_process").execFile(BACKEND_EXE_FILE, []);
    } else {
        subpy = require("child_process").spawn(
            "python", ["-m", "backend.backend"]
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
            if (useBinary) {
                if (x.COMM == BACKEND_EXE_FILE) {
                    process.kill(x.PID);
                }
            } else {
                if (x.COMM.endsWith("bin/python")) {
                    process.kill(x.PID);
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

const createMainWindow = () => {
    var url = 'http://localhost:8000/';
    mainWindow = new BrowserWindow({
        width: 500,
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
        mainWindow.loadURL(url);
    });
};

app.on("ready", function () {
    startPythonSubprocess();
    createMainWindow();
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
