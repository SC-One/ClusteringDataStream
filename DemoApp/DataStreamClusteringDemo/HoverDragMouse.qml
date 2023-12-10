import QtQuick 2.15

MouseArea {
    property bool isHoveredNow: true
    hoverEnabled: true
    onEntered: isHoveredNow = true
    onExited: isHoveredNow = false
    cursorShape: isHoveredNow ? Qt.DragMoveCursor : Qt.ArrowCursor
}
