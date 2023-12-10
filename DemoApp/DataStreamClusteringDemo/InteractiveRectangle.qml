import QtQuick 2.15

Rectangle {
    id: selComp
    property int rulersSize: 18
    property real minimumW: 30
    property real minimumH: 50

    border {
        width: 2
        color: "steelblue"
    }
    color: "transparent"

    Rectangle {
        anchors.fill: parent
        color: parent.border.color
        opacity: 0.1
    }
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onDoubleClicked: {
            parent.destroy()
        }
    }
    Rectangle {
        width: rulersSize
        height: rulersSize
        radius: rulersSize
        color: "steelblue"
        anchors.horizontalCenter: parent.left
        anchors.verticalCenter: parent.verticalCenter

        HoverDragMouse {
            anchors.fill: parent
            drag {
                target: parent
                axis: Drag.XAxis
            }
            onMouseXChanged: {
                if (drag.active) {
                    selComp.width = selComp.width - mouseX
                    selComp.x = selComp.x + mouseX
                    if (selComp.width < selComp.minimumW)
                        selComp.width = selComp.minimumW
                }
            }
        }
    }

    Rectangle {
        width: rulersSize
        height: rulersSize
        radius: rulersSize
        color: "steelblue"
        anchors.horizontalCenter: parent.right
        anchors.verticalCenter: parent.verticalCenter

        HoverDragMouse {
            anchors.fill: parent
            drag {
                target: parent
                axis: Drag.XAxis
            }
            onMouseXChanged: {
                if (drag.active) {
                    selComp.width = selComp.width + mouseX
                    if (selComp.width < selComp.minimumW)
                        selComp.width = selComp.minimumW
                }
            }
        }
    }

    Rectangle {
        width: rulersSize
        height: rulersSize
        radius: rulersSize
        x: parent.x / 2
        y: 0
        color: "steelblue"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.top

        HoverDragMouse {
            anchors.fill: parent
            drag {
                target: parent
                axis: Drag.YAxis
            }
            onMouseYChanged: {
                if (drag.active) {
                    selComp.height = selComp.height - mouseY
                    selComp.y = selComp.y + mouseY
                    if (selComp.height < selComp.minimumH)
                        selComp.height = selComp.minimumH
                }
            }
        }
    }

    Rectangle {
        width: rulersSize
        height: rulersSize
        radius: rulersSize
        x: parent.x / 2
        y: parent.y
        color: "steelblue"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.bottom

        HoverDragMouse {
            anchors.fill: parent
            drag {
                target: parent
                axis: Drag.YAxis
            }
            onMouseYChanged: {
                if (drag.active) {
                    selComp.height = selComp.height + mouseY
                    if (selComp.height < selComp.minimumH)
                        selComp.height = selComp.minimumH
                }
            }
        }
    }
}
