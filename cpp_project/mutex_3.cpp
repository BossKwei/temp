//
// Created by bosskwei on 18-9-29.
//

#include "utils.hpp"


std::mutex mtx;
std::condition_variable condition;
bool produced = false;
bool consumed = true;


void thread_producer(int num) {
    for (int i = 0; i < num; i += 1) {
        std::unique_lock<std::mutex> lock(mtx);
        condition.wait(lock, [=]() -> bool { return consumed; });

        auto producer = [=]() {
            std::cout << "producing " << i << std::endl;
            produced = true;
            consumed = false;
        };
        producer();

        condition.notify_one();
    }

}


void thread_consumer(int num) {
    for (int i = 0; i < num; i += 1) {
        std::unique_lock<std::mutex> lock(mtx);
        condition.wait(lock, [=]() -> bool { return produced; });

        auto consumer = [=]() {
            produced = false;
            consumed = true;
            std::cout << "consuming " << i << std::endl;
        };
        consumer();

        condition.notify_one();
    }
}


int main() {
    // producer and consumer one by one with condition_variable

    std::thread t1(thread_producer, 11);
    std::thread t2(thread_consumer, 10);

    t1.join();
    t2.join();

    return 0;
}
