//
// Created by bosskwei on 18-9-29.
//

#include "utils.hpp"


std::mutex mtx;
std::condition_variable condition;
int produced = 0;


void producer(int num) {
    for (int i = 0; i < num; i += 1) {
        std::unique_lock<std::mutex> lock(mtx);

        auto producer = [=]() {
            std::cout << "producing " << i << std::endl;
            produced += 1;
        };
        producer();

        condition.notify_one();
    }

}


void consumer(int num) {
    for (int i = 0; i < num; i += 1) {
        std::unique_lock<std::mutex> lock(mtx);
        condition.wait(lock, [=]() -> bool { return produced > 0; });

        auto consumer = [=]() {
            produced -= 1;
            std::cout << "consuming " << i << std::endl;
        };
        consumer();
    }
}


int main() {
    // producer and consumer async with condition_variable

    std::thread t1(producer, 10);
    std::thread t2(consumer, 3);
    std::thread t3(consumer, 7);

    t1.join();
    t2.join();
    t3.join();

    return 0;
}
