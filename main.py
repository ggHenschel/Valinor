#!/usr/bin/python3.6
import valinorapp, sys
import PyQt5.QtCore as QtCore

def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'INFO'
    elif mode == QtCore.QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    #print('line: %d, func: %s(), file: %s' % (
    #      context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))

QtCore.qInstallMessageHandler(qt_message_handler)

if __name__ == '__main__':
    #DO STUFF
    vln = valinorapp.ValinorApp(sys.argv)
    vln.run()

    sys.exit(vln.exec_())
