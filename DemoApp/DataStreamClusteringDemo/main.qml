import QtQuick 2.14
import QtQuick.Window 2.14

Window {
    id: window
    width: 640
    height: 480
    visible: true

    title: qsTr("Data Stream Clustering")

    Component.onCompleted: {
        window.showMaximized()
    }
}
