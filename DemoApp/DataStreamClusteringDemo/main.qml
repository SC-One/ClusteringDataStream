import QtQuick 2.15
import QtQuick.Window 2.15
import QtLocation 5.12
import QtPositioning 5.12
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.12

import QtQuick.Dialogs 1.1

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

    QtObject {
        id: interactiveVars
        property real defaultGeneratingInterval: 300 // ms
        property bool runningGenerateData: true
    }

    RowLayout {
        id: wholeAppRowLayout
        anchors.fill: parent
        spacing: 1

        Map {
            id: mapItem
            property real fixedSize: 10
            plugin: myPlugin
            Layout.fillWidth: true
            Layout.fillHeight: true
            center: QtPositioning.coordinate(35.6998, 51.3354) // azadi
            zoomLevel: 15

            minimumZoomLevel: 15
            maximumZoomLevel: 15
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
                acceptedButtons: Qt.LeftButton | Qt.MiddleButton
                onClicked: {
                    // add single point in the datastream
                    var point = Qt.point(mouse.x, mouse.y)
                    var pos = mapItem.mousePointToCordinate(point)

                    if (Qt.MiddleButton == mouse.button) {
                        rectangleModels.append({
                                                   "myId": rectangleModels.nextId(
                                                               ),
                                                   "lati": pos.latitude,
                                                   "longi": pos.longitude
                                               })
                        return
                    }

                    mouseMap.number += 1
                    var itemInList = {
                        "lati": pos.latitude,
                        "longi": pos.longitude,
                        "id": mouseMap.number.toString()
                        //                        ,
                        //                        "xClicked": mouseMap.mouseX,
                        //                        "yClicked": mouseMap.mouseY
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
                id: myItemViewForBounds
                property real scaleOfRectangle: 30
                model: ListModel {
                    id: rectangleModels
                    property int numberId: 2
                    function nextId() {
                        return ++numberId
                    }
                    function deleteTheItemOnID(id) {
                        for (var i = 0; i < rectangleModels.count; ++i) {
                            if (rectangleModels.get(i).myId == id) {
                                rectangleModels.remove(i)
                                return
                            }
                        }
                    }
                }

                delegate: MapQuickItem {
                    id: resizableItem
                    zoomLevel: 16
                    coordinate: QtPositioning.coordinate(lati, longi)
                    property point pointClicked: mapItem.fromCoordinate(
                                                     coordinate)
                    onCoordinateChanged: console.log(coordinate)
                    anchorPoint.x: width / 2
                    anchorPoint.y: height / 2
                    width: mapItem.fixedSize * myItemViewForBounds.scaleOfRectangle
                    height: mapItem.fixedSize * myItemViewForBounds.scaleOfRectangle
                    visible: true
                    sourceItem: Rectangle {
                        id: resizeHandle

                        width: mapItem.fixedSize * myItemViewForBounds.scaleOfRectangle
                        height: mapItem.fixedSize * myItemViewForBounds.scaleOfRectangle

                        border {
                            width: 8
                            color: "steelblue"
                        }
                        color: "transparent"

                        Rectangle {
                            anchors.fill: parent
                            color: parent.border.color
                            opacity: 0.1
                        }
                        property var topLeftCoord: mapItem.mouseToCordinate(
                                                       Math.max(
                                                           0,
                                                           resizableItem.pointClicked.x
                                                           - resizableItem.width / 4),
                                                       Math.max(
                                                           0,
                                                           resizableItem.pointClicked.y
                                                           - resizableItem.height / 4))
                        property var bottomRightCoord: mapItem.mouseToCordinate(
                                                           Math.max(
                                                               0,
                                                               resizableItem.pointClicked.x
                                                               + resizableItem.width / 4),
                                                           Math.max(
                                                               0,
                                                               resizableItem.pointClicked.y
                                                               + resizableItem.height / 4))
                        Timer {
                            id: boundedTimer
                            interval: interactiveVars.defaultGeneratingInterval
                            onTriggered: {
                                var leftTopCoord = parent.topLeftCoord
                                var rightBottomCoord = parent.bottomRightCoord
                                var randomX = leftTopCoord.latitude + Math.random(
                                            ) * (rightBottomCoord.latitude - leftTopCoord.latitude)
                                var randomY = leftTopCoord.longitude + Math.random(
                                            ) * (rightBottomCoord.longitude
                                                 - leftTopCoord.longitude)

                                mouseMap.number += 1
                                var itemInList = {
                                    "lati": randomX,
                                    "longi": randomY,
                                    "id": mouseMap.number.toString()
                                }
                                pointsModel.append(itemInList)
                                //                                console.log("Here I came", pointsModel.count,
                                //                                            randomX, randomY)
                            }
                            repeat: true
                            running: interactiveVars.runningGenerateData
                        }
                        MouseArea {
                            anchors.fill: parent
                            onDoubleClicked: {
                                rectangleModels.deleteTheItemOnID(myId)
                            }
                        }
                    }
                }
            }

            MapItemView {
                model: pointsModel
                delegate: MapQuickItem {
                    id: pointOnMap
                    coordinate: QtPositioning.coordinate(lati, longi)
                    anchorPoint.x: mapItem.fixedSize / 2
                    anchorPoint.y: mapItem.fixedSize / 2
                    sourceItem: Rectangle {
                        id: point
                        color: "red"
                        radius: 5
                        width: mapItem.fixedSize
                        height: mapItem.fixedSize
                    }
                }
            }
        }
    }
}
