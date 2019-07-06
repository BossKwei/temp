//
// Created by bosskwei on 18-9-29.
//

#include "utils.hpp"


class A {
public:
    A() {
        a_ = "0";
        std::cout << "A() construct " << this << std::endl;
    }

    explicit A(const std::string &a) {
        a_ = a;
        std::cout << "A(const std::string &a) construct " << this << std::endl;
    }

    // 拷贝构造函数，执行 A a2(a1) 后，若为浅拷贝，则 a1 和 a2 均持有指针
    A(const A &other) {
        a_ = other.a_;
        std::cout << "A(const A &other) construct " << this << std::endl;
    }

    // 移动构造函数，执行 A a2(a1) 后，若为浅拷贝，则 a2 持有指针，a1 不再引用指针
    // 即内部元素从 a1 转移到 a2
    A(A&& other) noexcept {
        a_ = std::move(other.a_);
        std::cout << "A(A&& other) construct " << this << std::endl;
    }

    ~A() {
        std::cout << "~A() destruct " << this << std::endl;
    }

private:
    std::string a_;
};


int main()
{
    {
        std::vector<A> l;
        l.push_back(std::move(A("123")));
    }
    std::cout << std::endl;
    {
        std::vector<A> l;
        l.emplace_back("123");
    }

    return 0;
}
