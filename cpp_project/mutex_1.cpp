//
// Created by bosskwei on 18-9-29.
//

#include "utils.hpp"


std::mutex mtx;
std::condition_variable condition;
bool produced = false;
bool consumed = true;


void worker_1() {
    for (int i = 0; i < 4; i += 1) {
        std::unique_lock<std::mutex> lock(mtx);
        condition.wait(lock, [=]() -> bool { return consumed; });

        auto producer = [=]() {
            std::cout << "producing " << i << std::endl << std::flush;
            produced = true;
            consumed = false;
        };
        producer();

        condition.notify_one();
    }

}


void worker_2() {
    for (int i = 0; i < 8; i += 1) {
        std::unique_lock<std::mutex> lock(mtx);
        condition.wait(lock, [=]() -> bool { return produced; });

        auto consumer = [=]() {
            produced = false;
            consumed = true;
            std::cout << "consuming " << i << std::endl << std::flush;
        };
        consumer();

        condition.notify_one();
    }
}


int g_counter = 0;


int main() {
    // example from cpp reference

    std::thread t1(worker_1);
    std::thread t2(worker_2);

    t1.join();
    t2.join();

    return 0;
}
