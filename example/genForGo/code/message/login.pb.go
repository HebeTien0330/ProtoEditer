// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.36.3
// 	protoc        v4.24.0
// source: login.proto

package message

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type C2SQueryServerList struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	No            int32                  `protobuf:"varint,1,opt,name=no,proto3" json:"no,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *C2SQueryServerList) Reset() {
	*x = C2SQueryServerList{}
	mi := &file_login_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *C2SQueryServerList) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*C2SQueryServerList) ProtoMessage() {}

func (x *C2SQueryServerList) ProtoReflect() protoreflect.Message {
	mi := &file_login_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use C2SQueryServerList.ProtoReflect.Descriptor instead.
func (*C2SQueryServerList) Descriptor() ([]byte, []int) {
	return file_login_proto_rawDescGZIP(), []int{0}
}

func (x *C2SQueryServerList) GetNo() int32 {
	if x != nil {
		return x.No
	}
	return 0
}

type S2CQueryServerList struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	No            int32                  `protobuf:"varint,1,opt,name=no,proto3" json:"no,omitempty"`
	Code          int32                  `protobuf:"varint,2,opt,name=code,proto3" json:"code,omitempty"`
	Data          string                 `protobuf:"bytes,3,opt,name=data,proto3" json:"data,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *S2CQueryServerList) Reset() {
	*x = S2CQueryServerList{}
	mi := &file_login_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *S2CQueryServerList) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*S2CQueryServerList) ProtoMessage() {}

func (x *S2CQueryServerList) ProtoReflect() protoreflect.Message {
	mi := &file_login_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use S2CQueryServerList.ProtoReflect.Descriptor instead.
func (*S2CQueryServerList) Descriptor() ([]byte, []int) {
	return file_login_proto_rawDescGZIP(), []int{1}
}

func (x *S2CQueryServerList) GetNo() int32 {
	if x != nil {
		return x.No
	}
	return 0
}

func (x *S2CQueryServerList) GetCode() int32 {
	if x != nil {
		return x.Code
	}
	return 0
}

func (x *S2CQueryServerList) GetData() string {
	if x != nil {
		return x.Data
	}
	return ""
}

type C2SLogin struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	No            int32                  `protobuf:"varint,1,opt,name=no,proto3" json:"no,omitempty"`
	UserId        string                 `protobuf:"bytes,2,opt,name=userId,proto3" json:"userId,omitempty"`
	ServerId      string                 `protobuf:"bytes,3,opt,name=serverId,proto3" json:"serverId,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *C2SLogin) Reset() {
	*x = C2SLogin{}
	mi := &file_login_proto_msgTypes[2]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *C2SLogin) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*C2SLogin) ProtoMessage() {}

func (x *C2SLogin) ProtoReflect() protoreflect.Message {
	mi := &file_login_proto_msgTypes[2]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use C2SLogin.ProtoReflect.Descriptor instead.
func (*C2SLogin) Descriptor() ([]byte, []int) {
	return file_login_proto_rawDescGZIP(), []int{2}
}

func (x *C2SLogin) GetNo() int32 {
	if x != nil {
		return x.No
	}
	return 0
}

func (x *C2SLogin) GetUserId() string {
	if x != nil {
		return x.UserId
	}
	return ""
}

func (x *C2SLogin) GetServerId() string {
	if x != nil {
		return x.ServerId
	}
	return ""
}

type S2CLogin struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	No            int32                  `protobuf:"varint,1,opt,name=no,proto3" json:"no,omitempty"`
	Code          int32                  `protobuf:"varint,2,opt,name=code,proto3" json:"code,omitempty"`
	UserId        string                 `protobuf:"bytes,3,opt,name=userId,proto3" json:"userId,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *S2CLogin) Reset() {
	*x = S2CLogin{}
	mi := &file_login_proto_msgTypes[3]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *S2CLogin) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*S2CLogin) ProtoMessage() {}

func (x *S2CLogin) ProtoReflect() protoreflect.Message {
	mi := &file_login_proto_msgTypes[3]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use S2CLogin.ProtoReflect.Descriptor instead.
func (*S2CLogin) Descriptor() ([]byte, []int) {
	return file_login_proto_rawDescGZIP(), []int{3}
}

func (x *S2CLogin) GetNo() int32 {
	if x != nil {
		return x.No
	}
	return 0
}

func (x *S2CLogin) GetCode() int32 {
	if x != nil {
		return x.Code
	}
	return 0
}

func (x *S2CLogin) GetUserId() string {
	if x != nil {
		return x.UserId
	}
	return ""
}

var File_login_proto protoreflect.FileDescriptor

var file_login_proto_rawDesc = []byte{
	0x0a, 0x0b, 0x6c, 0x6f, 0x67, 0x69, 0x6e, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x0e, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x63, 0x6f, 0x6c, 0x2e, 0x6c, 0x6f, 0x67, 0x69, 0x6e, 0x22, 0x24, 0x0a,
	0x12, 0x43, 0x32, 0x53, 0x51, 0x75, 0x65, 0x72, 0x79, 0x53, 0x65, 0x72, 0x76, 0x65, 0x72, 0x4c,
	0x69, 0x73, 0x74, 0x12, 0x0e, 0x0a, 0x02, 0x6e, 0x6f, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52,
	0x02, 0x6e, 0x6f, 0x22, 0x4c, 0x0a, 0x12, 0x53, 0x32, 0x43, 0x51, 0x75, 0x65, 0x72, 0x79, 0x53,
	0x65, 0x72, 0x76, 0x65, 0x72, 0x4c, 0x69, 0x73, 0x74, 0x12, 0x0e, 0x0a, 0x02, 0x6e, 0x6f, 0x18,
	0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x02, 0x6e, 0x6f, 0x12, 0x12, 0x0a, 0x04, 0x63, 0x6f, 0x64,
	0x65, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x52, 0x04, 0x63, 0x6f, 0x64, 0x65, 0x12, 0x12, 0x0a,
	0x04, 0x64, 0x61, 0x74, 0x61, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x64, 0x61, 0x74,
	0x61, 0x22, 0x4e, 0x0a, 0x08, 0x43, 0x32, 0x53, 0x4c, 0x6f, 0x67, 0x69, 0x6e, 0x12, 0x0e, 0x0a,
	0x02, 0x6e, 0x6f, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x02, 0x6e, 0x6f, 0x12, 0x16, 0x0a,
	0x06, 0x75, 0x73, 0x65, 0x72, 0x49, 0x64, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x06, 0x75,
	0x73, 0x65, 0x72, 0x49, 0x64, 0x12, 0x1a, 0x0a, 0x08, 0x73, 0x65, 0x72, 0x76, 0x65, 0x72, 0x49,
	0x64, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x08, 0x73, 0x65, 0x72, 0x76, 0x65, 0x72, 0x49,
	0x64, 0x22, 0x46, 0x0a, 0x08, 0x53, 0x32, 0x43, 0x4c, 0x6f, 0x67, 0x69, 0x6e, 0x12, 0x0e, 0x0a,
	0x02, 0x6e, 0x6f, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x02, 0x6e, 0x6f, 0x12, 0x12, 0x0a,
	0x04, 0x63, 0x6f, 0x64, 0x65, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x52, 0x04, 0x63, 0x6f, 0x64,
	0x65, 0x12, 0x16, 0x0a, 0x06, 0x75, 0x73, 0x65, 0x72, 0x49, 0x64, 0x18, 0x03, 0x20, 0x01, 0x28,
	0x09, 0x52, 0x06, 0x75, 0x73, 0x65, 0x72, 0x49, 0x64, 0x42, 0x0a, 0x5a, 0x08, 0x2f, 0x6d, 0x65,
	0x73, 0x73, 0x61, 0x67, 0x65, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_login_proto_rawDescOnce sync.Once
	file_login_proto_rawDescData = file_login_proto_rawDesc
)

func file_login_proto_rawDescGZIP() []byte {
	file_login_proto_rawDescOnce.Do(func() {
		file_login_proto_rawDescData = protoimpl.X.CompressGZIP(file_login_proto_rawDescData)
	})
	return file_login_proto_rawDescData
}

var file_login_proto_msgTypes = make([]protoimpl.MessageInfo, 4)
var file_login_proto_goTypes = []any{
	(*C2SQueryServerList)(nil), // 0: protocol.login.C2SQueryServerList
	(*S2CQueryServerList)(nil), // 1: protocol.login.S2CQueryServerList
	(*C2SLogin)(nil),           // 2: protocol.login.C2SLogin
	(*S2CLogin)(nil),           // 3: protocol.login.S2CLogin
}
var file_login_proto_depIdxs = []int32{
	0, // [0:0] is the sub-list for method output_type
	0, // [0:0] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_login_proto_init() }
func file_login_proto_init() {
	if File_login_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_login_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   4,
			NumExtensions: 0,
			NumServices:   0,
		},
		GoTypes:           file_login_proto_goTypes,
		DependencyIndexes: file_login_proto_depIdxs,
		MessageInfos:      file_login_proto_msgTypes,
	}.Build()
	File_login_proto = out.File
	file_login_proto_rawDesc = nil
	file_login_proto_goTypes = nil
	file_login_proto_depIdxs = nil
}
