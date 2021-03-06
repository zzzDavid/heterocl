/*!
 *  Copyright (c) 2017 by Contributors
 * \file rpc_server_env
 * \brief Server environment of the RPC.
 */
#include <tvm/runtime/registry.h>
#include "../file_util.h"

namespace TVM {
namespace runtime {

std::string RPCGetPath(const std::string& name) {
  static const PackedFunc* f =
      runtime::Registry::Get("tvm.contrib.rpc.server.workpath");
  CHECK(f != nullptr) << "require tvm.contrib.rpc.server.workpath";
  return (*f)(name);
}

TVM_REGISTER_GLOBAL("tvm.contrib.rpc.server.upload")
    .set_body([](TVMArgs args, TVMRetValue* rv) {
      std::string file_name = RPCGetPath(args[0]);
      std::string data = args[1];
      LOG(INFO) << "Upload " << file_name << "... nbytes=" << data.length();
      SaveBinaryToFile(file_name, data);
    });

TVM_REGISTER_GLOBAL("tvm.contrib.rpc.server.download")
    .set_body([](TVMArgs args, TVMRetValue* rv) {
      std::string file_name = RPCGetPath(args[0]);
      std::string data;
      LoadBinaryFromFile(file_name, &data);
      TVMByteArray arr;
      arr.data = data.c_str();
      arr.size = data.length();
      LOG(INFO) << "Download " << file_name << "... nbytes=" << arr.size;
      *rv = arr;
    });

}  // namespace runtime
}  // namespace TVM
