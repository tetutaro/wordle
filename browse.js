const {app, BrowserWindow} = require('electron')
const path = require('path')

function createWindow () {
    var appname = path.basename(process.argv[0])
    var url = 'http://localhost:8000/'
    const mainWindow = new BrowserWindow({
        width: 510,
        height: 750,
        resizable: false,
        icon: __dirname + '/icons/wordle.icns',
        webPreferences: {
            nodeIntegration: false
        }
    })
    mainWindow.setMenuBarVisibility(false)
    mainWindow.loadURL(url)
}

app.whenReady().then(() => {
    createWindow()
    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow()
        }
    })
})

app.on('window-all-closed', function () {
    app.quit()
})
