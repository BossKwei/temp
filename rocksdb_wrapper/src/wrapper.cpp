#include <cmath>
#include <string>
#include <iostream>
#include <unordered_map>

#include "rocksdb/db.h"
#include "rocksdb/slice.h"
#include "rocksdb/options.h"
#include "rocksdb/statistics.h"
#include "rocksdb/utilities/transaction.h"
#include "rocksdb/utilities/transaction_db.h"

namespace {
template <typename... Args>
std::string stringFormat(const std::string &format, Args... args) {
  size_t size = std::snprintf(nullptr, 0, format.c_str(), args...) +
                1; // Extra space for '\0'
  std::unique_ptr<char[]> buf(new char[size]);
  std::snprintf(buf.get(), size, format.c_str(), args...);
  return std::string(buf.get(),
                     buf.get() + size - 1); // We don't want the '\0' inside
}

void checkDatabase(const rocksdb::Status &s, const std::string &file,
                   size_t line) {
  if (!s.ok()) {
    std::string err =
        stringFormat("%s:%d - %s", file.c_str(), line, s.ToString().c_str());
    throw std::runtime_error(err);
  }
}

#define CHECK(s) checkDatabase(s, __FILE__, __LINE__)
}

class RocksDBWrapper {
public:
  RocksDBWrapper(const std::string &path, bool create_if_missing) : db_(nullptr), tx_(nullptr) {
    rocksdb::Options options;
    rocksdb::TransactionDBOptions db_options;
    options.create_if_missing = create_if_missing;
    options.statistics = rocksdb::CreateDBStatistics();
    CHECK(rocksdb::TransactionDB::Open(options, db_options, path, &(this->db_)));
    this->Rollback();
  }
  ~RocksDBWrapper() {
    std::string status;
    this->db_->GetProperty("rocksdb.stats", &status);
    std::cout << "---------- RocksDB Status ----------" << std::endl;
    std::cout << status << std::endl;
    std::cout << "------------------------------------" << std::endl;
    //
    delete this->tx_;
    delete this->db_;
  }

  std::string Get(const std::string &key) {
    std::string value;
    if (!key.length()) {
      return value;
    }
    rocksdb::Status s = this->tx_->GetForUpdate(this->read_options_, key, &value);
    if (s.IsNotFound()) {
      return value;
    }
    CHECK(s);
    return value;
  }

  void Set(const std::string &key, const std::string &value) {
    CHECK(this->tx_->Put(key, value));
  }

  void Rollback() {
      if (this->tx_) {
        delete this->tx_;
      }
      this->tx_ = db_->BeginTransaction(this->write_options_);
  }

  void Commit() {
    this->tx_->Commit();
    this->Rollback();
  }

private:
  rocksdb::TransactionDB *db_;
  rocksdb::Transaction *tx_;
  rocksdb::ReadOptions read_options_;
  rocksdb::WriteOptions write_options_;
};


namespace {
  size_t current_id = 0;
  std::unordered_map<size_t, RocksDBWrapper *> descriptor_map;
}

extern "C" {
  size_t rocksdb_open(const char *path, bool create_if_missing) {
    current_id += 1;
    descriptor_map[current_id] = new RocksDBWrapper(path, create_if_missing);
    return current_id;
  }

  size_t rocksdb_tx_get(size_t id, const char *key, char *value) {
    if (value == nullptr) {
      std::string result = descriptor_map[id]->Get(key);
      return result.length();
    }
    std::string result = descriptor_map[id]->Get(key);
    memcpy(value, result.c_str(), result.length());
    return result.length();
  }

  void rocksdb_tx_set(size_t id, const char *key, char *value) {
    descriptor_map[id]->Set(key, value);
  }

  void rocksdb_tx_rollback(size_t id) {
    descriptor_map[id]->Rollback();
  }

  void rocksdb_tx_commit(size_t id) {
    descriptor_map[id]->Commit();
  }

  void rocksdb_close(size_t id) {
    delete descriptor_map[id];
    descriptor_map.erase(id);
  }
}