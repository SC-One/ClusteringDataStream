#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlEngine>

#include <QLocale>
#include <QTranslator>

#include <Structures.h>

#include <DenStreamClusterer.h>

int main(int argc, char *argv[]) {
#if QT_VERSION < QT_VERSION_CHECK(6, 0, 0)
  QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
#endif
  QGuiApplication app(argc, argv);

  qRegisterMetaType<Message>("Message");
  qRegisterMetaType<Point>("Point");
  qmlRegisterType<DenStreamClusterer>("ir.HCoding.SocietyCleaner", 1, 0,
                                      "DenStreamClusterer");
  QTranslator translator;
  const QStringList uiLanguages = QLocale::system().uiLanguages();
  for (const QString &locale : uiLanguages) {
#ifdef PRJ_ROOT_NAME
    static const QString prefixName = PRJ_ROOT_NAME;
#endif
    const QString baseName = prefixName + "_" + QLocale(locale).name();
    if (translator.load(":/i18n/" + baseName)) {
      app.installTranslator(&translator);
      break;
    }
  }

  QQmlApplicationEngine engine;
  const QUrl url(QStringLiteral("qrc:/main.qml"));
  QObject::connect(
      &engine, &QQmlApplicationEngine::objectCreated, &app,
      [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
          QCoreApplication::exit(-1);
      },
      Qt::QueuedConnection);
  engine.load(url);

  return app.exec();
}
