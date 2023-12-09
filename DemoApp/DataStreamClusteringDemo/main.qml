import QtQuick 2.15
import QtQuick.Window 2.15
import QtLocation 5.12
import QtPositioning 5.12
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.12

import QtQuick.Dialogs 1.1

import QtQuick.Dialogs 1.2

Window {
    id: windowRoot
    width: Qt.platform.os == "android" ? Screen.width : 512
    height: Qt.platform.os == "android" ? Screen.height : 512
    Component.onCompleted: {
        if (Qt.platform.os != "android")
            windowRoot.showMaximized()
    }
    visible: true
    title: qsTr("Data stream Clustering")

    MessageDialog {
        id: thrownMsgBox
        visible: false
        icon: StandardIcon.Critical
        title: "Error thrown"
        text: "DenStream.lastError"
    }

    Plugin {
        id: myPlugin
        name: "osm" // "mapboxgl", "esri", ...
    }

    ListModel {
        id: pointsModel
    }

    RowLayout {
        id: wholeAppRowLayout
        anchors.fill: parent
        spacing: 1

        Map {
            id: mapItem
            plugin: myPlugin
            Layout.fillWidth: true
            Layout.fillHeight: true
            center: QtPositioning.coordinate(35.6998, 51.3354) // azadi
            zoomLevel: 15
            function mouseToCordinate(x = 125, y = 111) {
                var point = Qt.point(x, y)
                return mapItem.toCoordinate(point)
            }

            function mousePointToCordinate(mouseVal) {
                var point = Qt.point(mouseVal.x, mouseVal.y)
                return mapItem.toCoordinate(point)
            }

            MouseArea {
                id: mouseMap
                property int number: 0 // 0 is reserved
                anchors.fill: parent
                onClicked: {
                    // add single point in the datastream
                    var point = Qt.point(mouse.x, mouse.y)
                    var pos = mapItem.mousePointToCordinate(point)
                    mouseMap.number += 1
                    var itemInList = {
                        "lati": pos.latitude,
                        "longi": pos.longitude,
                        "id": mouseMap.number.toString(),
                        "xClicked": mouseMap.mouseX,
                        "yClicked": mouseMap.mouseY
                    }
                    pointsModel.append(itemInList)
                    console.log(point, "\t", pos, "\t", itemInList)
                }
            }
            function reloadPan() {
                mapItem.pan(1, 1)
                mapItem.pan(-1, -1)
            }
            onHeightChanged: mapItem.reloadPan()
            onWidthChanged: mapItem.reloadPan()

            MapItemView {
                model: 2
                delegate: MapQuickItem {
                    coordinate: QtPositioning.coordinate(
                                    35.6900 + index * 0.01, 51.3300)
                    anchorPoint.x: point.width / 2
                    anchorPoint.y: point.height / 2
                    sourceItem: Rectangle {
                        color: "green"
                        radius: 3
                        width: 75
                        height: 45
                    }
                }
            }
            MapItemView {
                model: pointsModel
                delegate: MapQuickItem {
                    id: pointOnMap
                    coordinate: QtPositioning.coordinate(lati, longi)
                    anchorPoint.x: point.width / 2
                    anchorPoint.y: point.height / 2
                    sourceItem: Rectangle {
                        id: point
                        color: "red"
                        radius: 5
                        width: 10
                        height: 10
                    }
                }
            }
        }
    }
}
