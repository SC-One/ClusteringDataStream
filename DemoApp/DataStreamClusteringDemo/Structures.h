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

#endif // STRUCTURES_H
