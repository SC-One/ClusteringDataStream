cmake_minimum_required(VERSION 3.14)

set(PRJ_ROOT_NAME DataStreamClusteringDemo)
project(${PRJ_ROOT_NAME} VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core Quick LinguistTools WebSockets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Quick LinguistTools WebSockets)

set(TS_FILES ${PRJ_ROOT_NAME}_fa_IR.ts)

set(PROJECT_SOURCES
  main.cpp
  qml.qrc
  ${TS_FILES}
)

if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
  qt_add_executable(${PRJ_ROOT_NAME}
    MANUAL_FINALIZATION
    ${PROJECT_SOURCES}
  )
# Define target properties for Android with Qt 6 as:
#    set_property(TARGET ${PRJ_ROOT_NAME} APPEND PROPERTY QT_ANDROID_PACKAGE_SOURCE_DIR
#                 ${CMAKE_CURRENT_SOURCE_DIR}/android)
# For more information, see https://doc.qt.io/qt-6/qt-add-executable.html#target-creation

qt_create_translation(QM_FILES ${CMAKE_SOURCE_DIR} ${TS_FILES})
else()
  if(ANDROID)
    add_library(${PRJ_ROOT_NAME} SHARED
      ${PROJECT_SOURCES}
    )
  # Define properties for Android with Qt 5 after find_package() calls as:
  #    set(ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android")
else()
  add_executable(${PRJ_ROOT_NAME}
    ${PROJECT_SOURCES}
    SocketClient.h SocketClient.cpp
    Structures.h
    Parser.h Parser.cpp
    ThreadSafeQueue.h ThreadSafeQueue.cpp
    DenStreamClusterer.h DenStreamClusterer.cpp
  )
endif()

qt5_create_translation(QM_FILES ${CMAKE_SOURCE_DIR} ${TS_FILES})
endif()

target_link_libraries(${PRJ_ROOT_NAME} PRIVATE
  Qt${QT_VERSION_MAJOR}::Core
  Qt${QT_VERSION_MAJOR}::Quick
  Qt${QT_VERSION_MAJOR}::WebSockets
)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
if(${QT_VERSION} VERSION_LESS 6.1.0)
  set(BUNDLE_ID_OPTION MACOSX_BUNDLE_GUI_IDENTIFIER com.example.${PRJ_ROOT_NAME})
endif()
set_target_properties(${PRJ_ROOT_NAME} PROPERTIES
  ${BUNDLE_ID_OPTION}
  MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
  MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
  MACOSX_BUNDLE TRUE
  WIN32_EXECUTABLE TRUE
)

#include(GNUInstallDirs)
#install(TARGETS ${PRJ_ROOT_NAME}
#    BUNDLE DESTINATION .
#    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

if(QT_VERSION_MAJOR EQUAL 6)
  qt_import_qml_plugins(${PRJ_ROOT_NAME})
  qt_finalize_executable(${PRJ_ROOT_NAME})
endif()



target_compile_definitions(${PRJ_ROOT_NAME} PUBLIC -DPRJ_ROOT_NAME="${PRJ_ROOT_NAME}")
target_include_directories(${PRJ_ROOT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
