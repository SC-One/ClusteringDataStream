#ifndef PARSER_H
#define PARSER_H

#include <QByteArray>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QObject>
#include <Structures.h>

class Parser : public QObject {
  Q_OBJECT
public:
  static QJsonArray pointToJson(const Point &point);

  static Point jsonToPoint(const QJsonObject &obj);

  static QByteArray messageToJson(const Message &message);

  static ClusterLabel parseMessage(const QString &msg);

private:
  static QByteArray toJsonText(QJsonObject const &item);
};

#endif // PARSER_H
