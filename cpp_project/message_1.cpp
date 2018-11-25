//
// Created by bosskwei on 18-9-30.
//

#include "utils.hpp"


namespace message {
    class BaseMessage {
    public:
        BaseMessage() = default;
        explicit BaseMessage(std::string info) : info_(std::move(info)) {}
        virtual ~BaseMessage() = default;

        std::string info() {
            return info_;
        }
    private:
        std::string info_;
    };

    class CPUMessage : public BaseMessage {
    public:
        CPUMessage() : BaseMessage() {};
        explicit CPUMessage(const std::string &info) : BaseMessage(info) {}
    };

    class GPUMessage : public BaseMessage {
    public:
        GPUMessage() : BaseMessage() {};
        explicit GPUMessage(const std::string &info) : BaseMessage(info) {}
    };
}


namespace loop {
    class EventLoop {
    public:
        template<class MessageType>
        void publishMessage(const std::string &url,
                            const MessageType &msg) {
            events_.emplace(url, std::dynamic_pointer_cast<message::BaseMessage>(msg));
        }

        template<class MessageType>
        void addSubscriber(const std::string &url, const std::function<void(std::shared_ptr<MessageType>)> &callback) {
            mapping_[url].push_back([=](const std::shared_ptr<message::BaseMessage> &msg) {
                callback(std::dynamic_pointer_cast<MessageType>(msg));
            });
        }

        void pollOnce() {
            if (!events_.empty()) {
                std::string url;
                std::shared_ptr<message::BaseMessage> msg;
                std::tie(url, msg) = events_.front();
                events_.pop();

                if (mapping_.find(url) != mapping_.end()) {
                    for (const auto &callback : mapping_[url]) {
                        callback(msg);
                    }
                }
            }
        }

    private:
        // event = (url, msg)
        std::queue<std::tuple<std::string, std::shared_ptr<message::BaseMessage>>> events_;
        // mapping = (url, [callback_1, callback_2, ...])
        std::unordered_map<std::string,
                std::vector<std::function<void(std::shared_ptr<message::BaseMessage>)>>> mapping_;
    };
}


class Handler {
public:
    void cpu_message_received(const std::shared_ptr<message::CPUMessage> &msg) {
        if (not check_msg(msg)) {
            return;
        }
        std::cout << "call handle_cpu_message() " << msg->info() << std::endl;
    }

    void gpu_message_received(const std::shared_ptr<message::GPUMessage> &msg) {
        if (not check_msg(msg)) {
            return;
        }
        std::cout << "call handle_gpu_message() " << msg->info() << std::endl;
    }

private:
    template <typename MessageType>
    bool check_msg(const std::shared_ptr<MessageType> &msg) {
        if (not msg) {
            std::cerr << "check_msg() error: ";
            std::cerr << "dynamic_pointer_cast wrong and msg type is mismatched" << std::endl;
            return false;
        }
        return true;
    }
};


int main() {
    loop::EventLoop loop;
    Handler handler;

    loop.addSubscriber<message::CPUMessage>("/system/cpu",
                                            std::bind(&Handler::cpu_message_received, handler, std::placeholders::_1));
    loop.addSubscriber<message::GPUMessage>("/system/gpu",
                                            std::bind(&Handler::gpu_message_received, handler, std::placeholders::_1));

    loop.publishMessage("/system/cpu", std::make_shared<message::CPUMessage>("cpu msg test"));
    loop.pollOnce();
    loop.publishMessage("/system/gpu", std::make_shared<message::GPUMessage>("gpu msg test"));
    loop.pollOnce();
    loop.publishMessage("/system/gpu", std::make_shared<message::CPUMessage>("gpu msg test"));
    loop.pollOnce();

    return 0;
}
