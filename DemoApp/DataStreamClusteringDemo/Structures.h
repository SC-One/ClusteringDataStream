#ifndef STRUCTURES_H
#define STRUCTURES_H
#include <QString>

struct Point {
  double x;
  double y;
};

struct Message {
  QString id;
  Point point;
};

struct ClusterLabel {
  QString id;
  Point point;
  int cluster;
};

// struct Cordinate {
//  Q_GADGET
//  double mLatitude;
//  double mLongitude;
//  Q_PROPERTY(double latitude MEMBER mLatitude)
//  Q_PROPERTY(double longitude MEMBER mLongitude)
//};
// Q_DECLARE_METATYPE(MyStruct)

#endif // STRUCTURES_H
