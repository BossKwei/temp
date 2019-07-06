#include <iostream>
#include <string>

#include "rocksdb/db.h"
#include "rocksdb/options.h"
#include "rocksdb/slice.h"
#include "rocksdb/utilities/transaction.h"
#include "rocksdb/utilities/transaction_db.h"

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

void test_tx_write() {
  rocksdb::Options options;
  options.create_if_missing = true;
  rocksdb::TransactionDBOptions db_options;
  rocksdb::TransactionDB *db;
  CHECK(rocksdb::TransactionDB::Open(options, db_options, "tmp_db", &db));

  // inside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;
    rocksdb::Transaction *tx = db->BeginTransaction(write_options);

    std::string value;
    s = tx->Get(read_options, "a", &value);
    assert(s.IsNotFound());

    CHECK(tx->Put("a", "1"));

    CHECK(tx->Commit());
    delete tx;
  }

  // outside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;

    std::string value;
    s = db->Get(read_options, "a", &value);
    assert(s.ok());
  }

  delete db;
  CHECK(rocksdb::DestroyDB("tmp_db", options));
}

void test_tx_write_multi() {
  rocksdb::Options options;
  options.create_if_missing = true;
  rocksdb::TransactionDBOptions db_options;
  rocksdb::TransactionDB *db;
  CHECK(rocksdb::TransactionDB::Open(options, db_options, "tmp_db", &db));

  // inside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;
    rocksdb::Transaction *tx = db->BeginTransaction(write_options);

    std::string value;
    s = tx->Get(read_options, "a", &value);
    assert(s.IsNotFound());

    CHECK(tx->Put("a", "1"));
    CHECK(tx->Put("a", "2"));
    CHECK(tx->Put("a", "3"));

    CHECK(tx->Commit());
    delete tx;
  }

  // outside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;

    std::string value;
    s = db->Get(read_options, "a", &value);
    assert(s.ok());
    assert(value == "3");
  }

  delete db;
  CHECK(rocksdb::DestroyDB("tmp_db", options));
}

void test_tx_write_not_commit() {
  rocksdb::Options options;
  options.create_if_missing = true;
  rocksdb::TransactionDBOptions db_options;
  rocksdb::TransactionDB *db;
  CHECK(rocksdb::TransactionDB::Open(options, db_options, "tmp_db", &db));

  // inside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;
    rocksdb::Transaction *tx = db->BeginTransaction(write_options);

    std::string value1;
    s = tx->Get(read_options, "a", &value1);
    assert(s.IsNotFound());

    CHECK(tx->Put("a", "1"));

    std::string value2;
    s = tx->Get(read_options, "a", &value2);
    assert(s.ok());
    assert(value2 == "1");

    delete tx;
  }

  // outside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;

    std::string value;
    s = db->Get(read_options, "a", &value);
    assert(s.IsNotFound());
  }

  delete db;
  CHECK(rocksdb::DestroyDB("tmp_db", options));
}

void test_tx_read_after_db_write() {
  rocksdb::Options options;
  options.create_if_missing = true;
  rocksdb::TransactionDBOptions db_options;
  rocksdb::TransactionDB *db;
  CHECK(rocksdb::TransactionDB::Open(options, db_options, "tmp_db", &db));

  // inside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;
    rocksdb::Transaction *tx = db->BeginTransaction(write_options);

    // inside transaction
    std::string value1;
    s = tx->Get(read_options, "a", &value1);
    assert(s.IsNotFound());

    // outside transaction
    { CHECK(db->Put(write_options, "a", "1")); }

    // inside transaction
    std::string value2;
    s = tx->Get(read_options, "a", &value2);
    assert(s.ok());
    assert(value2 == "1");

    delete tx;
  }

  delete db;
  CHECK(rocksdb::DestroyDB("tmp_db", options));
}

void test_tx_read_for_update_locked() {
  rocksdb::Options options;
  options.create_if_missing = true;
  rocksdb::TransactionDBOptions db_options;
  rocksdb::TransactionDB *db;
  CHECK(rocksdb::TransactionDB::Open(options, db_options, "tmp_db", &db));

  // outside transaction
  {
    rocksdb::WriteOptions write_options;
    CHECK(db->Put(write_options, "a", "100"));
  }

  // inside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;
    rocksdb::Transaction *tx = db->BeginTransaction(write_options);

    std::string value1;
    s = tx->GetForUpdate(read_options, "a", &value1);
    assert(s.ok());
    assert(value1 == "100");

    // outside transaction
    {
      s = db->Put(write_options, "a", "99");
      assert(s.IsTimedOut());
      // > Operation timed out: Timeout waiting to lock key
    }

    delete tx;
  }

  delete db;
  CHECK(rocksdb::DestroyDB("tmp_db", options));
}

void test_tx_read_for_update_success() {
  rocksdb::Options options;
  options.create_if_missing = true;
  rocksdb::TransactionDBOptions db_options;
  rocksdb::TransactionDB *db;
  CHECK(rocksdb::TransactionDB::Open(options, db_options, "tmp_db", &db));

  // outside transaction
  {
    rocksdb::WriteOptions write_options;
    CHECK(db->Put(write_options, "a", "100"));
  }

  // inside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;
    rocksdb::Transaction *tx = db->BeginTransaction(write_options);

    std::string value;
    s = tx->GetForUpdate(read_options, "a", &value);
    assert(s.ok());
    assert(value == "100");

    CHECK(tx->Put("a", "1"));
    CHECK(tx->Commit());

    delete tx;
  }

  // outside transaction
  {
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;

    std::string value1;
    CHECK(db->Get(read_options, "a", &value1));
    assert(value1 == "1");

    CHECK(db->Put(write_options, "a", "100"));

    std::string value2;
    CHECK(db->Get(read_options, "a", &value2));
    assert(value2 == "100");
  }

  delete db;
  CHECK(rocksdb::DestroyDB("tmp_db", options));
}

void test_tx_read_write_with_snapshot() {
  rocksdb::Options options;
  options.create_if_missing = true;
  rocksdb::TransactionDBOptions db_options;
  rocksdb::TransactionDB *db;
  CHECK(rocksdb::TransactionDB::Open(options, db_options, "tmp_db", &db));

  // inside transaction
  {
    rocksdb::Status s;
    rocksdb::ReadOptions read_options;
    rocksdb::WriteOptions write_options;
    rocksdb::TransactionOptions tx_options;
    tx_options.set_snapshot = true;
    rocksdb::Transaction *tx = db->BeginTransaction(write_options, tx_options);
    const rocksdb::Snapshot *snapshot = tx->GetSnapshot();

    // inside transaction
    std::string value1;
    read_options.snapshot = snapshot;
    s = tx->Get(read_options, "a", &value1);
    assert(s.IsNotFound());

    // outside transaction
    { CHECK(db->Put(write_options, "a", "1")); }

    // inside transaction
    std::string value2;
    read_options.snapshot = snapshot;
    s = tx->Get(read_options, "a", &value2);
    assert(s.IsNotFound());

    delete tx;
  }

  delete db;
  CHECK(rocksdb::DestroyDB("tmp_db", options));
}

void test_rocksdb_transaction_wrapper() {}

int main() {
  /*********************************************
   * TX need to call commit explicit.
   **********************************************/
  test_tx_write();
  test_tx_write_multi();
  test_tx_write_not_commit();
  /*********************************************
   * DB write could affect tx read; To solve this,
   * we need to use snapshot.
   **********************************************/
  test_tx_read_after_db_write();
  /*********************************************
   * TX exclusive lock db on current key;
   * only current tx finish operation on this key,
   * any else could continue operate on it.
   **********************************************/
  test_tx_read_for_update_locked();
  test_tx_read_for_update_success();
  /*********************************************
   * TX read with / without snapshot
   **********************************************/
  test_tx_read_write_with_snapshot();
  /*********************************************
   * Wrapper for rocksdb transaction
   **********************************************/
  test_rocksdb_transaction_wrapper();
}
