#include "Parser.h"

#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>

QJsonArray Parser::pointToJson(const Point &point) {
  QJsonArray arr;
  arr.append(point.x);
  arr.append(point.y);
  return arr;
}

Point Parser::jsonToPoint(const QJsonArray &obj) {
  Point point;
  point.x = obj[0].toDouble();
  point.y = obj[1].toDouble();
  return point;
}

QByteArray Parser::messageToJson(const Message &message) {
  QJsonObject obj;
  obj["id"] = message.id;
  obj["point"] = pointToJson(message.point);
  return toJsonText(obj);
}

ClusterLabel Parser::parseMessage(const QString &msg) {
  auto doc = QJsonDocument::fromJson(msg.toUtf8());
  QJsonObject obj = doc.object();
  ClusterLabel result;
  result.id = obj["id"].toString();
  result.cluster = obj["cluster"].toInt();
  result.point = jsonToPoint(obj["point"].toArray());
  return result;
}

QByteArray Parser::toJsonText(const QJsonObject &item) {
  QJsonDocument doc;
  doc.setObject(item);
  return doc.toJson();
}
