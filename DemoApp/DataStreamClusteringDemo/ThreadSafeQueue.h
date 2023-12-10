#ifndef THREADSAFEQUEUE_H
#define THREADSAFEQUEUE_H
#include <atomic>
#include <iostream>
#include <queue>
#include <thread>

class Spinlock {
public:
  void lock() {
    while (flag.test_and_set(std::memory_order_acquire)) {
    }
  }

  void unlock() { flag.clear(std::memory_order_release); }

private:
  std::atomic_flag flag = ATOMIC_FLAG_INIT;
};

template <typename T> class ThreadSafeQueue {
public:
  void enqueue(const T &data) {
    spinlock.lock();
    queue.push(data);
    spinlock.unlock();
  }

  bool dequeue(T &result) {
    spinlock.lock();
    if (queue.empty()) {
      spinlock.unlock();
      return false;
    }

    result = queue.front();
    queue.pop();
    spinlock.unlock();
    return true;
  }

  bool isEmpty() {
    spinlock.lock();
    bool empty = queue.empty();
    spinlock.unlock();
    return empty;
  }

private:
  std::queue<T> queue;
  Spinlock spinlock;
};

#endif // THREADSAFEQUEUE_H
