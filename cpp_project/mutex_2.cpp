//
// Created by bosskwei on 18-9-29.
//

#include "utils.hpp"


std::mutex mtx_producer;
std::mutex mtx_consumer;


void init() {
    mtx_consumer.lock();
}


void worker_1() {
    for (int i = 0; i < 100001; i += 1) {
        {
            mtx_producer.lock();
            std::cout << "worker_1 running " << i << std::endl;
            // std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        {
            mtx_consumer.unlock();
        }
    }
    std::cout << "worker_1 end" << std::endl;
}


void worker_2() {
    for (int i = 0; i < 100000; i += 1) {
        {
            mtx_consumer.lock();
            std::cout << "worker_2 running " << i << std::endl;
            // std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        {
            mtx_producer.unlock();
        }
    }
    std::cout << "worker_2 end" << std::endl;
}


int main()
{
    // producer and consumer one by one with two mutex

    init();
    std::thread t1(worker_1);
    std::thread t2(worker_2);
    t1.join();
    t2.join();
    return 0;
}
