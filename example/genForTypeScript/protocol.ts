export interface MessageWrapper {
  c2s_gm?: C2SGm;
  s2c_gm?: S2CGm;
  c2s_heartbeat?: C2SHeartbeat;
  s2c_heartbeat?: S2CHeartbeat;
  c2s_query_leaderboard?: C2SQueryLeaderboard;
  s2c_query_leaderboard?: S2CQueryLeaderboard;
  c2s_query_server_list?: C2SQueryServerList;
  s2c_query_server_list?: S2CQueryServerList;
  c2s_login?: C2SLogin;
  s2c_login?: S2CLogin;
  c2s_query_player_data?: C2SQueryPlayerData;
  s2c_query_player_data?: S2CQueryPlayerData;
  c2s_query_player_basic?: C2SQueryPlayerBasic;
  s2c_query_player_basic?: S2CQueryPlayerBasic;
}

export function encodeMessageWrapper(message: MessageWrapper): Uint8Array {
  let bb = popByteBuffer();
  _encodeMessageWrapper(message, bb);
  return toUint8Array(bb);
}

function _encodeMessageWrapper(message: MessageWrapper, bb: ByteBuffer): void {
  // optional C2SGm c2s_gm = 1001;
  let $c2s_gm = message.c2s_gm;
  if ($c2s_gm !== undefined) {
    writeVarint32(bb, 8010);
    let nested = popByteBuffer();
    _encodeC2SGm($c2s_gm, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional S2CGm s2c_gm = 1002;
  let $s2c_gm = message.s2c_gm;
  if ($s2c_gm !== undefined) {
    writeVarint32(bb, 8018);
    let nested = popByteBuffer();
    _encodeS2CGm($s2c_gm, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional C2SHeartbeat c2s_heartbeat = 1003;
  let $c2s_heartbeat = message.c2s_heartbeat;
  if ($c2s_heartbeat !== undefined) {
    writeVarint32(bb, 8026);
    let nested = popByteBuffer();
    _encodeC2SHeartbeat($c2s_heartbeat, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional S2CHeartbeat s2c_heartbeat = 1004;
  let $s2c_heartbeat = message.s2c_heartbeat;
  if ($s2c_heartbeat !== undefined) {
    writeVarint32(bb, 8034);
    let nested = popByteBuffer();
    _encodeS2CHeartbeat($s2c_heartbeat, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional C2SQueryLeaderboard c2s_query_leaderboard = 1005;
  let $c2s_query_leaderboard = message.c2s_query_leaderboard;
  if ($c2s_query_leaderboard !== undefined) {
    writeVarint32(bb, 8042);
    let nested = popByteBuffer();
    _encodeC2SQueryLeaderboard($c2s_query_leaderboard, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional S2CQueryLeaderboard s2c_query_leaderboard = 1006;
  let $s2c_query_leaderboard = message.s2c_query_leaderboard;
  if ($s2c_query_leaderboard !== undefined) {
    writeVarint32(bb, 8050);
    let nested = popByteBuffer();
    _encodeS2CQueryLeaderboard($s2c_query_leaderboard, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional C2SQueryServerList c2s_query_server_list = 1007;
  let $c2s_query_server_list = message.c2s_query_server_list;
  if ($c2s_query_server_list !== undefined) {
    writeVarint32(bb, 8058);
    let nested = popByteBuffer();
    _encodeC2SQueryServerList($c2s_query_server_list, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional S2CQueryServerList s2c_query_server_list = 1008;
  let $s2c_query_server_list = message.s2c_query_server_list;
  if ($s2c_query_server_list !== undefined) {
    writeVarint32(bb, 8066);
    let nested = popByteBuffer();
    _encodeS2CQueryServerList($s2c_query_server_list, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional C2SLogin c2s_login = 1009;
  let $c2s_login = message.c2s_login;
  if ($c2s_login !== undefined) {
    writeVarint32(bb, 8074);
    let nested = popByteBuffer();
    _encodeC2SLogin($c2s_login, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional S2CLogin s2c_login = 1010;
  let $s2c_login = message.s2c_login;
  if ($s2c_login !== undefined) {
    writeVarint32(bb, 8082);
    let nested = popByteBuffer();
    _encodeS2CLogin($s2c_login, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional C2SQueryPlayerData c2s_query_player_data = 1011;
  let $c2s_query_player_data = message.c2s_query_player_data;
  if ($c2s_query_player_data !== undefined) {
    writeVarint32(bb, 8090);
    let nested = popByteBuffer();
    _encodeC2SQueryPlayerData($c2s_query_player_data, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional S2CQueryPlayerData s2c_query_player_data = 1012;
  let $s2c_query_player_data = message.s2c_query_player_data;
  if ($s2c_query_player_data !== undefined) {
    writeVarint32(bb, 8098);
    let nested = popByteBuffer();
    _encodeS2CQueryPlayerData($s2c_query_player_data, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional C2SQueryPlayerBasic c2s_query_player_basic = 1013;
  let $c2s_query_player_basic = message.c2s_query_player_basic;
  if ($c2s_query_player_basic !== undefined) {
    writeVarint32(bb, 8106);
    let nested = popByteBuffer();
    _encodeC2SQueryPlayerBasic($c2s_query_player_basic, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }

  // optional S2CQueryPlayerBasic s2c_query_player_basic = 1014;
  let $s2c_query_player_basic = message.s2c_query_player_basic;
  if ($s2c_query_player_basic !== undefined) {
    writeVarint32(bb, 8114);
    let nested = popByteBuffer();
    _encodeS2CQueryPlayerBasic($s2c_query_player_basic, nested);
    writeVarint32(bb, nested.limit);
    writeByteBuffer(bb, nested);
    pushByteBuffer(nested);
  }
}

export function decodeMessageWrapper(binary: Uint8Array): MessageWrapper {
  return _decodeMessageWrapper(wrapByteBuffer(binary));
}

function _decodeMessageWrapper(bb: ByteBuffer): MessageWrapper {
  let message: MessageWrapper = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional C2SGm c2s_gm = 1001;
      case 1001: {
        let limit = pushTemporaryLength(bb);
        message.c2s_gm = _decodeC2SGm(bb);
        bb.limit = limit;
        break;
      }

      // optional S2CGm s2c_gm = 1002;
      case 1002: {
        let limit = pushTemporaryLength(bb);
        message.s2c_gm = _decodeS2CGm(bb);
        bb.limit = limit;
        break;
      }

      // optional C2SHeartbeat c2s_heartbeat = 1003;
      case 1003: {
        let limit = pushTemporaryLength(bb);
        message.c2s_heartbeat = _decodeC2SHeartbeat(bb);
        bb.limit = limit;
        break;
      }

      // optional S2CHeartbeat s2c_heartbeat = 1004;
      case 1004: {
        let limit = pushTemporaryLength(bb);
        message.s2c_heartbeat = _decodeS2CHeartbeat(bb);
        bb.limit = limit;
        break;
      }

      // optional C2SQueryLeaderboard c2s_query_leaderboard = 1005;
      case 1005: {
        let limit = pushTemporaryLength(bb);
        message.c2s_query_leaderboard = _decodeC2SQueryLeaderboard(bb);
        bb.limit = limit;
        break;
      }

      // optional S2CQueryLeaderboard s2c_query_leaderboard = 1006;
      case 1006: {
        let limit = pushTemporaryLength(bb);
        message.s2c_query_leaderboard = _decodeS2CQueryLeaderboard(bb);
        bb.limit = limit;
        break;
      }

      // optional C2SQueryServerList c2s_query_server_list = 1007;
      case 1007: {
        let limit = pushTemporaryLength(bb);
        message.c2s_query_server_list = _decodeC2SQueryServerList(bb);
        bb.limit = limit;
        break;
      }

      // optional S2CQueryServerList s2c_query_server_list = 1008;
      case 1008: {
        let limit = pushTemporaryLength(bb);
        message.s2c_query_server_list = _decodeS2CQueryServerList(bb);
        bb.limit = limit;
        break;
      }

      // optional C2SLogin c2s_login = 1009;
      case 1009: {
        let limit = pushTemporaryLength(bb);
        message.c2s_login = _decodeC2SLogin(bb);
        bb.limit = limit;
        break;
      }

      // optional S2CLogin s2c_login = 1010;
      case 1010: {
        let limit = pushTemporaryLength(bb);
        message.s2c_login = _decodeS2CLogin(bb);
        bb.limit = limit;
        break;
      }

      // optional C2SQueryPlayerData c2s_query_player_data = 1011;
      case 1011: {
        let limit = pushTemporaryLength(bb);
        message.c2s_query_player_data = _decodeC2SQueryPlayerData(bb);
        bb.limit = limit;
        break;
      }

      // optional S2CQueryPlayerData s2c_query_player_data = 1012;
      case 1012: {
        let limit = pushTemporaryLength(bb);
        message.s2c_query_player_data = _decodeS2CQueryPlayerData(bb);
        bb.limit = limit;
        break;
      }

      // optional C2SQueryPlayerBasic c2s_query_player_basic = 1013;
      case 1013: {
        let limit = pushTemporaryLength(bb);
        message.c2s_query_player_basic = _decodeC2SQueryPlayerBasic(bb);
        bb.limit = limit;
        break;
      }

      // optional S2CQueryPlayerBasic s2c_query_player_basic = 1014;
      case 1014: {
        let limit = pushTemporaryLength(bb);
        message.s2c_query_player_basic = _decodeS2CQueryPlayerBasic(bb);
        bb.limit = limit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface C2SGm {
  no?: number;
  userId?: string;
  cmd?: string;
  args?: { [key: string]: string };
}

export function encodeC2SGm(message: C2SGm): Uint8Array {
  let bb = popByteBuffer();
  _encodeC2SGm(message, bb);
  return toUint8Array(bb);
}

function _encodeC2SGm(message: C2SGm, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional string userId = 2;
  let $userId = message.userId;
  if ($userId !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $userId);
  }

  // optional string cmd = 3;
  let $cmd = message.cmd;
  if ($cmd !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $cmd);
  }

  // optional map<string, string> args = 4;
  let map$args = message.args;
  if (map$args !== undefined) {
    for (let key in map$args) {
      let nested = popByteBuffer();
      let value = map$args[key];
      writeVarint32(nested, 10);
      writeString(nested, key);
      writeVarint32(nested, 18);
      writeString(nested, value);
      writeVarint32(bb, 34);
      writeVarint32(bb, nested.offset);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }
}

export function decodeC2SGm(binary: Uint8Array): C2SGm {
  return _decodeC2SGm(wrapByteBuffer(binary));
}

function _decodeC2SGm(bb: ByteBuffer): C2SGm {
  let message: C2SGm = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional string userId = 2;
      case 2: {
        message.userId = readString(bb, readVarint32(bb));
        break;
      }

      // optional string cmd = 3;
      case 3: {
        message.cmd = readString(bb, readVarint32(bb));
        break;
      }

      // optional map<string, string> args = 4;
      case 4: {
        let values = message.args || (message.args = {});
        let outerLimit = pushTemporaryLength(bb);
        let key: string | undefined;
        let value: string | undefined;
        end_of_entry: while (!isAtEnd(bb)) {
          let tag = readVarint32(bb);
          switch (tag >>> 3) {
            case 0:
              break end_of_entry;
            case 1: {
              key = readString(bb, readVarint32(bb));
              break;
            }
            case 2: {
              value = readString(bb, readVarint32(bb));
              break;
            }
            default:
              skipUnknownField(bb, tag & 7);
          }
        }
        if (key === undefined || value === undefined)
          throw new Error("Invalid data for map: args");
        values[key] = value;
        bb.limit = outerLimit;
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface S2CGm {
  no?: number;
  code?: number;
  result?: string;
  remote?: string;
}

export function encodeS2CGm(message: S2CGm): Uint8Array {
  let bb = popByteBuffer();
  _encodeS2CGm(message, bb);
  return toUint8Array(bb);
}

function _encodeS2CGm(message: S2CGm, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional int32 code = 2;
  let $code = message.code;
  if ($code !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($code));
  }

  // optional string result = 3;
  let $result = message.result;
  if ($result !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $result);
  }

  // optional string remote = 4;
  let $remote = message.remote;
  if ($remote !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $remote);
  }
}

export function decodeS2CGm(binary: Uint8Array): S2CGm {
  return _decodeS2CGm(wrapByteBuffer(binary));
}

function _decodeS2CGm(bb: ByteBuffer): S2CGm {
  let message: S2CGm = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional int32 code = 2;
      case 2: {
        message.code = readVarint32(bb);
        break;
      }

      // optional string result = 3;
      case 3: {
        message.result = readString(bb, readVarint32(bb));
        break;
      }

      // optional string remote = 4;
      case 4: {
        message.remote = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface C2SHeartbeat {
  no?: number;
  timestamp?: string;
}

export function encodeC2SHeartbeat(message: C2SHeartbeat): Uint8Array {
  let bb = popByteBuffer();
  _encodeC2SHeartbeat(message, bb);
  return toUint8Array(bb);
}

function _encodeC2SHeartbeat(message: C2SHeartbeat, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional string timestamp = 2;
  let $timestamp = message.timestamp;
  if ($timestamp !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $timestamp);
  }
}

export function decodeC2SHeartbeat(binary: Uint8Array): C2SHeartbeat {
  return _decodeC2SHeartbeat(wrapByteBuffer(binary));
}

function _decodeC2SHeartbeat(bb: ByteBuffer): C2SHeartbeat {
  let message: C2SHeartbeat = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional string timestamp = 2;
      case 2: {
        message.timestamp = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface S2CHeartbeat {
  no?: number;
  code?: number;
}

export function encodeS2CHeartbeat(message: S2CHeartbeat): Uint8Array {
  let bb = popByteBuffer();
  _encodeS2CHeartbeat(message, bb);
  return toUint8Array(bb);
}

function _encodeS2CHeartbeat(message: S2CHeartbeat, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional int32 code = 2;
  let $code = message.code;
  if ($code !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($code));
  }
}

export function decodeS2CHeartbeat(binary: Uint8Array): S2CHeartbeat {
  return _decodeS2CHeartbeat(wrapByteBuffer(binary));
}

function _decodeS2CHeartbeat(bb: ByteBuffer): S2CHeartbeat {
  let message: S2CHeartbeat = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional int32 code = 2;
      case 2: {
        message.code = readVarint32(bb);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface C2SQueryLeaderboard {
  no?: number;
  userId?: string;
  name?: string;
  from?: number;
  to?: number;
}

export function encodeC2SQueryLeaderboard(message: C2SQueryLeaderboard): Uint8Array {
  let bb = popByteBuffer();
  _encodeC2SQueryLeaderboard(message, bb);
  return toUint8Array(bb);
}

function _encodeC2SQueryLeaderboard(message: C2SQueryLeaderboard, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional string userId = 2;
  let $userId = message.userId;
  if ($userId !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $userId);
  }

  // optional string name = 3;
  let $name = message.name;
  if ($name !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $name);
  }

  // optional int32 from = 4;
  let $from = message.from;
  if ($from !== undefined) {
    writeVarint32(bb, 32);
    writeVarint64(bb, intToLong($from));
  }

  // optional int32 to = 5;
  let $to = message.to;
  if ($to !== undefined) {
    writeVarint32(bb, 40);
    writeVarint64(bb, intToLong($to));
  }
}

export function decodeC2SQueryLeaderboard(binary: Uint8Array): C2SQueryLeaderboard {
  return _decodeC2SQueryLeaderboard(wrapByteBuffer(binary));
}

function _decodeC2SQueryLeaderboard(bb: ByteBuffer): C2SQueryLeaderboard {
  let message: C2SQueryLeaderboard = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional string userId = 2;
      case 2: {
        message.userId = readString(bb, readVarint32(bb));
        break;
      }

      // optional string name = 3;
      case 3: {
        message.name = readString(bb, readVarint32(bb));
        break;
      }

      // optional int32 from = 4;
      case 4: {
        message.from = readVarint32(bb);
        break;
      }

      // optional int32 to = 5;
      case 5: {
        message.to = readVarint32(bb);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface S2CQueryLeaderboard {
  no?: number;
  code?: number;
  data?: string;
}

export function encodeS2CQueryLeaderboard(message: S2CQueryLeaderboard): Uint8Array {
  let bb = popByteBuffer();
  _encodeS2CQueryLeaderboard(message, bb);
  return toUint8Array(bb);
}

function _encodeS2CQueryLeaderboard(message: S2CQueryLeaderboard, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional int32 code = 2;
  let $code = message.code;
  if ($code !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($code));
  }

  // optional string data = 3;
  let $data = message.data;
  if ($data !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $data);
  }
}

export function decodeS2CQueryLeaderboard(binary: Uint8Array): S2CQueryLeaderboard {
  return _decodeS2CQueryLeaderboard(wrapByteBuffer(binary));
}

function _decodeS2CQueryLeaderboard(bb: ByteBuffer): S2CQueryLeaderboard {
  let message: S2CQueryLeaderboard = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional int32 code = 2;
      case 2: {
        message.code = readVarint32(bb);
        break;
      }

      // optional string data = 3;
      case 3: {
        message.data = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface C2SQueryServerList {
  no?: number;
}

export function encodeC2SQueryServerList(message: C2SQueryServerList): Uint8Array {
  let bb = popByteBuffer();
  _encodeC2SQueryServerList(message, bb);
  return toUint8Array(bb);
}

function _encodeC2SQueryServerList(message: C2SQueryServerList, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }
}

export function decodeC2SQueryServerList(binary: Uint8Array): C2SQueryServerList {
  return _decodeC2SQueryServerList(wrapByteBuffer(binary));
}

function _decodeC2SQueryServerList(bb: ByteBuffer): C2SQueryServerList {
  let message: C2SQueryServerList = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface S2CQueryServerList {
  no?: number;
  code?: number;
  data?: string;
}

export function encodeS2CQueryServerList(message: S2CQueryServerList): Uint8Array {
  let bb = popByteBuffer();
  _encodeS2CQueryServerList(message, bb);
  return toUint8Array(bb);
}

function _encodeS2CQueryServerList(message: S2CQueryServerList, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional int32 code = 2;
  let $code = message.code;
  if ($code !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($code));
  }

  // optional string data = 3;
  let $data = message.data;
  if ($data !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $data);
  }
}

export function decodeS2CQueryServerList(binary: Uint8Array): S2CQueryServerList {
  return _decodeS2CQueryServerList(wrapByteBuffer(binary));
}

function _decodeS2CQueryServerList(bb: ByteBuffer): S2CQueryServerList {
  let message: S2CQueryServerList = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional int32 code = 2;
      case 2: {
        message.code = readVarint32(bb);
        break;
      }

      // optional string data = 3;
      case 3: {
        message.data = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface C2SLogin {
  no?: number;
  userId?: string;
  serverId?: string;
}

export function encodeC2SLogin(message: C2SLogin): Uint8Array {
  let bb = popByteBuffer();
  _encodeC2SLogin(message, bb);
  return toUint8Array(bb);
}

function _encodeC2SLogin(message: C2SLogin, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional string userId = 2;
  let $userId = message.userId;
  if ($userId !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $userId);
  }

  // optional string serverId = 3;
  let $serverId = message.serverId;
  if ($serverId !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $serverId);
  }
}

export function decodeC2SLogin(binary: Uint8Array): C2SLogin {
  return _decodeC2SLogin(wrapByteBuffer(binary));
}

function _decodeC2SLogin(bb: ByteBuffer): C2SLogin {
  let message: C2SLogin = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional string userId = 2;
      case 2: {
        message.userId = readString(bb, readVarint32(bb));
        break;
      }

      // optional string serverId = 3;
      case 3: {
        message.serverId = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface S2CLogin {
  no?: number;
  code?: number;
  userId?: string;
}

export function encodeS2CLogin(message: S2CLogin): Uint8Array {
  let bb = popByteBuffer();
  _encodeS2CLogin(message, bb);
  return toUint8Array(bb);
}

function _encodeS2CLogin(message: S2CLogin, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional int32 code = 2;
  let $code = message.code;
  if ($code !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($code));
  }

  // optional string userId = 3;
  let $userId = message.userId;
  if ($userId !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $userId);
  }
}

export function decodeS2CLogin(binary: Uint8Array): S2CLogin {
  return _decodeS2CLogin(wrapByteBuffer(binary));
}

function _decodeS2CLogin(bb: ByteBuffer): S2CLogin {
  let message: S2CLogin = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional int32 code = 2;
      case 2: {
        message.code = readVarint32(bb);
        break;
      }

      // optional string userId = 3;
      case 3: {
        message.userId = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface C2SQueryPlayerData {
  no?: number;
  userId?: string;
}

export function encodeC2SQueryPlayerData(message: C2SQueryPlayerData): Uint8Array {
  let bb = popByteBuffer();
  _encodeC2SQueryPlayerData(message, bb);
  return toUint8Array(bb);
}

function _encodeC2SQueryPlayerData(message: C2SQueryPlayerData, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional string userId = 2;
  let $userId = message.userId;
  if ($userId !== undefined) {
    writeVarint32(bb, 18);
    writeString(bb, $userId);
  }
}

export function decodeC2SQueryPlayerData(binary: Uint8Array): C2SQueryPlayerData {
  return _decodeC2SQueryPlayerData(wrapByteBuffer(binary));
}

function _decodeC2SQueryPlayerData(bb: ByteBuffer): C2SQueryPlayerData {
  let message: C2SQueryPlayerData = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional string userId = 2;
      case 2: {
        message.userId = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface S2CQueryPlayerData {
  no?: number;
  code?: number;
  data?: { [key: string]: string };
  remote?: string;
}

export function encodeS2CQueryPlayerData(message: S2CQueryPlayerData): Uint8Array {
  let bb = popByteBuffer();
  _encodeS2CQueryPlayerData(message, bb);
  return toUint8Array(bb);
}

function _encodeS2CQueryPlayerData(message: S2CQueryPlayerData, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional int32 code = 2;
  let $code = message.code;
  if ($code !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($code));
  }

  // optional map<string, string> data = 3;
  let map$data = message.data;
  if (map$data !== undefined) {
    for (let key in map$data) {
      let nested = popByteBuffer();
      let value = map$data[key];
      writeVarint32(nested, 10);
      writeString(nested, key);
      writeVarint32(nested, 18);
      writeString(nested, value);
      writeVarint32(bb, 26);
      writeVarint32(bb, nested.offset);
      writeByteBuffer(bb, nested);
      pushByteBuffer(nested);
    }
  }

  // optional string remote = 4;
  let $remote = message.remote;
  if ($remote !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $remote);
  }
}

export function decodeS2CQueryPlayerData(binary: Uint8Array): S2CQueryPlayerData {
  return _decodeS2CQueryPlayerData(wrapByteBuffer(binary));
}

function _decodeS2CQueryPlayerData(bb: ByteBuffer): S2CQueryPlayerData {
  let message: S2CQueryPlayerData = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional int32 code = 2;
      case 2: {
        message.code = readVarint32(bb);
        break;
      }

      // optional map<string, string> data = 3;
      case 3: {
        let values = message.data || (message.data = {});
        let outerLimit = pushTemporaryLength(bb);
        let key: string | undefined;
        let value: string | undefined;
        end_of_entry: while (!isAtEnd(bb)) {
          let tag = readVarint32(bb);
          switch (tag >>> 3) {
            case 0:
              break end_of_entry;
            case 1: {
              key = readString(bb, readVarint32(bb));
              break;
            }
            case 2: {
              value = readString(bb, readVarint32(bb));
              break;
            }
            default:
              skipUnknownField(bb, tag & 7);
          }
        }
        if (key === undefined || value === undefined)
          throw new Error("Invalid data for map: data");
        values[key] = value;
        bb.limit = outerLimit;
        break;
      }

      // optional string remote = 4;
      case 4: {
        message.remote = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface C2SQueryPlayerBasic {
  no?: number;
  users?: string[];
}

export function encodeC2SQueryPlayerBasic(message: C2SQueryPlayerBasic): Uint8Array {
  let bb = popByteBuffer();
  _encodeC2SQueryPlayerBasic(message, bb);
  return toUint8Array(bb);
}

function _encodeC2SQueryPlayerBasic(message: C2SQueryPlayerBasic, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // repeated string users = 2;
  let array$users = message.users;
  if (array$users !== undefined) {
    for (let value of array$users) {
      writeVarint32(bb, 18);
      writeString(bb, value);
    }
  }
}

export function decodeC2SQueryPlayerBasic(binary: Uint8Array): C2SQueryPlayerBasic {
  return _decodeC2SQueryPlayerBasic(wrapByteBuffer(binary));
}

function _decodeC2SQueryPlayerBasic(bb: ByteBuffer): C2SQueryPlayerBasic {
  let message: C2SQueryPlayerBasic = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // repeated string users = 2;
      case 2: {
        let values = message.users || (message.users = []);
        values.push(readString(bb, readVarint32(bb)));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface S2CQueryPlayerBasic {
  no?: number;
  code?: number;
  data?: string;
  remote?: string;
}

export function encodeS2CQueryPlayerBasic(message: S2CQueryPlayerBasic): Uint8Array {
  let bb = popByteBuffer();
  _encodeS2CQueryPlayerBasic(message, bb);
  return toUint8Array(bb);
}

function _encodeS2CQueryPlayerBasic(message: S2CQueryPlayerBasic, bb: ByteBuffer): void {
  // optional int32 no = 1;
  let $no = message.no;
  if ($no !== undefined) {
    writeVarint32(bb, 8);
    writeVarint64(bb, intToLong($no));
  }

  // optional int32 code = 2;
  let $code = message.code;
  if ($code !== undefined) {
    writeVarint32(bb, 16);
    writeVarint64(bb, intToLong($code));
  }

  // optional string data = 3;
  let $data = message.data;
  if ($data !== undefined) {
    writeVarint32(bb, 26);
    writeString(bb, $data);
  }

  // optional string remote = 4;
  let $remote = message.remote;
  if ($remote !== undefined) {
    writeVarint32(bb, 34);
    writeString(bb, $remote);
  }
}

export function decodeS2CQueryPlayerBasic(binary: Uint8Array): S2CQueryPlayerBasic {
  return _decodeS2CQueryPlayerBasic(wrapByteBuffer(binary));
}

function _decodeS2CQueryPlayerBasic(bb: ByteBuffer): S2CQueryPlayerBasic {
  let message: S2CQueryPlayerBasic = {} as any;

  end_of_message: while (!isAtEnd(bb)) {
    let tag = readVarint32(bb);

    switch (tag >>> 3) {
      case 0:
        break end_of_message;

      // optional int32 no = 1;
      case 1: {
        message.no = readVarint32(bb);
        break;
      }

      // optional int32 code = 2;
      case 2: {
        message.code = readVarint32(bb);
        break;
      }

      // optional string data = 3;
      case 3: {
        message.data = readString(bb, readVarint32(bb));
        break;
      }

      // optional string remote = 4;
      case 4: {
        message.remote = readString(bb, readVarint32(bb));
        break;
      }

      default:
        skipUnknownField(bb, tag & 7);
    }
  }

  return message;
}

export interface Long {
  low: number;
  high: number;
  unsigned: boolean;
}

interface ByteBuffer {
  bytes: Uint8Array;
  offset: number;
  limit: number;
}

function pushTemporaryLength(bb: ByteBuffer): number {
  let length = readVarint32(bb);
  let limit = bb.limit;
  bb.limit = bb.offset + length;
  return limit;
}

function skipUnknownField(bb: ByteBuffer, type: number): void {
  switch (type) {
    case 0: while (readByte(bb) & 0x80) { } break;
    case 2: skip(bb, readVarint32(bb)); break;
    case 5: skip(bb, 4); break;
    case 1: skip(bb, 8); break;
    default: throw new Error("Unimplemented type: " + type);
  }
}

function stringToLong(value: string): Long {
  return {
    low: value.charCodeAt(0) | (value.charCodeAt(1) << 16),
    high: value.charCodeAt(2) | (value.charCodeAt(3) << 16),
    unsigned: false,
  };
}

function longToString(value: Long): string {
  let low = value.low;
  let high = value.high;
  return String.fromCharCode(
    low & 0xFFFF,
    low >>> 16,
    high & 0xFFFF,
    high >>> 16);
}

// The code below was modified from https://github.com/protobufjs/bytebuffer.js
// which is under the Apache License 2.0.

let f32 = new Float32Array(1);
let f32_u8 = new Uint8Array(f32.buffer);

let f64 = new Float64Array(1);
let f64_u8 = new Uint8Array(f64.buffer);

function intToLong(value: number): Long {
  value |= 0;
  return {
    low: value,
    high: value >> 31,
    unsigned: value >= 0,
  };
}

let bbStack: ByteBuffer[] = [];

function popByteBuffer(): ByteBuffer {
  const bb = bbStack.pop();
  if (!bb) return { bytes: new Uint8Array(64), offset: 0, limit: 0 };
  bb.offset = bb.limit = 0;
  return bb;
}

function pushByteBuffer(bb: ByteBuffer): void {
  bbStack.push(bb);
}

function wrapByteBuffer(bytes: Uint8Array): ByteBuffer {
  return { bytes, offset: 0, limit: bytes.length };
}

function toUint8Array(bb: ByteBuffer): Uint8Array {
  let bytes = bb.bytes;
  let limit = bb.limit;
  return bytes.length === limit ? bytes : bytes.subarray(0, limit);
}

function skip(bb: ByteBuffer, offset: number): void {
  if (bb.offset + offset > bb.limit) {
    throw new Error('Skip past limit');
  }
  bb.offset += offset;
}

function isAtEnd(bb: ByteBuffer): boolean {
  return bb.offset >= bb.limit;
}

function grow(bb: ByteBuffer, count: number): number {
  let bytes = bb.bytes;
  let offset = bb.offset;
  let limit = bb.limit;
  let finalOffset = offset + count;
  if (finalOffset > bytes.length) {
    let newBytes = new Uint8Array(finalOffset * 2);
    newBytes.set(bytes);
    bb.bytes = newBytes;
  }
  bb.offset = finalOffset;
  if (finalOffset > limit) {
    bb.limit = finalOffset;
  }
  return offset;
}

function advance(bb: ByteBuffer, count: number): number {
  let offset = bb.offset;
  if (offset + count > bb.limit) {
    throw new Error('Read past limit');
  }
  bb.offset += count;
  return offset;
}

function readBytes(bb: ByteBuffer, count: number): Uint8Array {
  let offset = advance(bb, count);
  return bb.bytes.subarray(offset, offset + count);
}

function writeBytes(bb: ByteBuffer, buffer: Uint8Array): void {
  let offset = grow(bb, buffer.length);
  bb.bytes.set(buffer, offset);
}

function readString(bb: ByteBuffer, count: number): string {
  // Sadly a hand-coded UTF8 decoder is much faster than subarray+TextDecoder in V8
  let offset = advance(bb, count);
  let fromCharCode = String.fromCharCode;
  let bytes = bb.bytes;
  let invalid = '\uFFFD';
  let text = '';

  for (let i = 0; i < count; i++) {
    let c1 = bytes[i + offset], c2: number, c3: number, c4: number, c: number;

    // 1 byte
    if ((c1 & 0x80) === 0) {
      text += fromCharCode(c1);
    }

    // 2 bytes
    else if ((c1 & 0xE0) === 0xC0) {
      if (i + 1 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        if ((c2 & 0xC0) !== 0x80) text += invalid;
        else {
          c = ((c1 & 0x1F) << 6) | (c2 & 0x3F);
          if (c < 0x80) text += invalid;
          else {
            text += fromCharCode(c);
            i++;
          }
        }
      }
    }

    // 3 bytes
    else if ((c1 & 0xF0) == 0xE0) {
      if (i + 2 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        c3 = bytes[i + offset + 2];
        if (((c2 | (c3 << 8)) & 0xC0C0) !== 0x8080) text += invalid;
        else {
          c = ((c1 & 0x0F) << 12) | ((c2 & 0x3F) << 6) | (c3 & 0x3F);
          if (c < 0x0800 || (c >= 0xD800 && c <= 0xDFFF)) text += invalid;
          else {
            text += fromCharCode(c);
            i += 2;
          }
        }
      }
    }

    // 4 bytes
    else if ((c1 & 0xF8) == 0xF0) {
      if (i + 3 >= count) text += invalid;
      else {
        c2 = bytes[i + offset + 1];
        c3 = bytes[i + offset + 2];
        c4 = bytes[i + offset + 3];
        if (((c2 | (c3 << 8) | (c4 << 16)) & 0xC0C0C0) !== 0x808080) text += invalid;
        else {
          c = ((c1 & 0x07) << 0x12) | ((c2 & 0x3F) << 0x0C) | ((c3 & 0x3F) << 0x06) | (c4 & 0x3F);
          if (c < 0x10000 || c > 0x10FFFF) text += invalid;
          else {
            c -= 0x10000;
            text += fromCharCode((c >> 10) + 0xD800, (c & 0x3FF) + 0xDC00);
            i += 3;
          }
        }
      }
    }

    else text += invalid;
  }

  return text;
}

function writeString(bb: ByteBuffer, text: string): void {
  // Sadly a hand-coded UTF8 encoder is much faster than TextEncoder+set in V8
  let n = text.length;
  let byteCount = 0;

  // Write the byte count first
  for (let i = 0; i < n; i++) {
    let c = text.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF && i + 1 < n) {
      c = (c << 10) + text.charCodeAt(++i) - 0x35FDC00;
    }
    byteCount += c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4;
  }
  writeVarint32(bb, byteCount);

  let offset = grow(bb, byteCount);
  let bytes = bb.bytes;

  // Then write the bytes
  for (let i = 0; i < n; i++) {
    let c = text.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF && i + 1 < n) {
      c = (c << 10) + text.charCodeAt(++i) - 0x35FDC00;
    }
    if (c < 0x80) {
      bytes[offset++] = c;
    } else {
      if (c < 0x800) {
        bytes[offset++] = ((c >> 6) & 0x1F) | 0xC0;
      } else {
        if (c < 0x10000) {
          bytes[offset++] = ((c >> 12) & 0x0F) | 0xE0;
        } else {
          bytes[offset++] = ((c >> 18) & 0x07) | 0xF0;
          bytes[offset++] = ((c >> 12) & 0x3F) | 0x80;
        }
        bytes[offset++] = ((c >> 6) & 0x3F) | 0x80;
      }
      bytes[offset++] = (c & 0x3F) | 0x80;
    }
  }
}

function writeByteBuffer(bb: ByteBuffer, buffer: ByteBuffer): void {
  let offset = grow(bb, buffer.limit);
  let from = bb.bytes;
  let to = buffer.bytes;

  // This for loop is much faster than subarray+set on V8
  for (let i = 0, n = buffer.limit; i < n; i++) {
    from[i + offset] = to[i];
  }
}

function readByte(bb: ByteBuffer): number {
  return bb.bytes[advance(bb, 1)];
}

function writeByte(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 1);
  bb.bytes[offset] = value;
}

function readFloat(bb: ByteBuffer): number {
  let offset = advance(bb, 4);
  let bytes = bb.bytes;

  // Manual copying is much faster than subarray+set in V8
  f32_u8[0] = bytes[offset++];
  f32_u8[1] = bytes[offset++];
  f32_u8[2] = bytes[offset++];
  f32_u8[3] = bytes[offset++];
  return f32[0];
}

function writeFloat(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 4);
  let bytes = bb.bytes;
  f32[0] = value;

  // Manual copying is much faster than subarray+set in V8
  bytes[offset++] = f32_u8[0];
  bytes[offset++] = f32_u8[1];
  bytes[offset++] = f32_u8[2];
  bytes[offset++] = f32_u8[3];
}

function readDouble(bb: ByteBuffer): number {
  let offset = advance(bb, 8);
  let bytes = bb.bytes;

  // Manual copying is much faster than subarray+set in V8
  f64_u8[0] = bytes[offset++];
  f64_u8[1] = bytes[offset++];
  f64_u8[2] = bytes[offset++];
  f64_u8[3] = bytes[offset++];
  f64_u8[4] = bytes[offset++];
  f64_u8[5] = bytes[offset++];
  f64_u8[6] = bytes[offset++];
  f64_u8[7] = bytes[offset++];
  return f64[0];
}

function writeDouble(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 8);
  let bytes = bb.bytes;
  f64[0] = value;

  // Manual copying is much faster than subarray+set in V8
  bytes[offset++] = f64_u8[0];
  bytes[offset++] = f64_u8[1];
  bytes[offset++] = f64_u8[2];
  bytes[offset++] = f64_u8[3];
  bytes[offset++] = f64_u8[4];
  bytes[offset++] = f64_u8[5];
  bytes[offset++] = f64_u8[6];
  bytes[offset++] = f64_u8[7];
}

function readInt32(bb: ByteBuffer): number {
  let offset = advance(bb, 4);
  let bytes = bb.bytes;
  return (
    bytes[offset] |
    (bytes[offset + 1] << 8) |
    (bytes[offset + 2] << 16) |
    (bytes[offset + 3] << 24)
  );
}

function writeInt32(bb: ByteBuffer, value: number): void {
  let offset = grow(bb, 4);
  let bytes = bb.bytes;
  bytes[offset] = value;
  bytes[offset + 1] = value >> 8;
  bytes[offset + 2] = value >> 16;
  bytes[offset + 3] = value >> 24;
}

function readInt64(bb: ByteBuffer, unsigned: boolean): Long {
  return {
    low: readInt32(bb),
    high: readInt32(bb),
    unsigned,
  };
}

function writeInt64(bb: ByteBuffer, value: Long): void {
  writeInt32(bb, value.low);
  writeInt32(bb, value.high);
}

function readVarint32(bb: ByteBuffer): number {
  let c = 0;
  let value = 0;
  let b: number;
  do {
    b = readByte(bb);
    if (c < 32) value |= (b & 0x7F) << c;
    c += 7;
  } while (b & 0x80);
  return value;
}

function writeVarint32(bb: ByteBuffer, value: number): void {
  value >>>= 0;
  while (value >= 0x80) {
    writeByte(bb, (value & 0x7f) | 0x80);
    value >>>= 7;
  }
  writeByte(bb, value);
}

function readVarint64(bb: ByteBuffer, unsigned: boolean): Long {
  let part0 = 0;
  let part1 = 0;
  let part2 = 0;
  let b: number;

  b = readByte(bb); part0 = (b & 0x7F); if (b & 0x80) {
    b = readByte(bb); part0 |= (b & 0x7F) << 7; if (b & 0x80) {
      b = readByte(bb); part0 |= (b & 0x7F) << 14; if (b & 0x80) {
        b = readByte(bb); part0 |= (b & 0x7F) << 21; if (b & 0x80) {

          b = readByte(bb); part1 = (b & 0x7F); if (b & 0x80) {
            b = readByte(bb); part1 |= (b & 0x7F) << 7; if (b & 0x80) {
              b = readByte(bb); part1 |= (b & 0x7F) << 14; if (b & 0x80) {
                b = readByte(bb); part1 |= (b & 0x7F) << 21; if (b & 0x80) {

                  b = readByte(bb); part2 = (b & 0x7F); if (b & 0x80) {
                    b = readByte(bb); part2 |= (b & 0x7F) << 7;
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  return {
    low: part0 | (part1 << 28),
    high: (part1 >>> 4) | (part2 << 24),
    unsigned,
  };
}

function writeVarint64(bb: ByteBuffer, value: Long): void {
  let part0 = value.low >>> 0;
  let part1 = ((value.low >>> 28) | (value.high << 4)) >>> 0;
  let part2 = value.high >>> 24;

  // ref: src/google/protobuf/io/coded_stream.cc
  let size =
    part2 === 0 ?
      part1 === 0 ?
        part0 < 1 << 14 ?
          part0 < 1 << 7 ? 1 : 2 :
          part0 < 1 << 21 ? 3 : 4 :
        part1 < 1 << 14 ?
          part1 < 1 << 7 ? 5 : 6 :
          part1 < 1 << 21 ? 7 : 8 :
      part2 < 1 << 7 ? 9 : 10;

  let offset = grow(bb, size);
  let bytes = bb.bytes;

  switch (size) {
    case 10: bytes[offset + 9] = (part2 >>> 7) & 0x01;
    case 9: bytes[offset + 8] = size !== 9 ? part2 | 0x80 : part2 & 0x7F;
    case 8: bytes[offset + 7] = size !== 8 ? (part1 >>> 21) | 0x80 : (part1 >>> 21) & 0x7F;
    case 7: bytes[offset + 6] = size !== 7 ? (part1 >>> 14) | 0x80 : (part1 >>> 14) & 0x7F;
    case 6: bytes[offset + 5] = size !== 6 ? (part1 >>> 7) | 0x80 : (part1 >>> 7) & 0x7F;
    case 5: bytes[offset + 4] = size !== 5 ? part1 | 0x80 : part1 & 0x7F;
    case 4: bytes[offset + 3] = size !== 4 ? (part0 >>> 21) | 0x80 : (part0 >>> 21) & 0x7F;
    case 3: bytes[offset + 2] = size !== 3 ? (part0 >>> 14) | 0x80 : (part0 >>> 14) & 0x7F;
    case 2: bytes[offset + 1] = size !== 2 ? (part0 >>> 7) | 0x80 : (part0 >>> 7) & 0x7F;
    case 1: bytes[offset] = size !== 1 ? part0 | 0x80 : part0 & 0x7F;
  }
}

function readVarint32ZigZag(bb: ByteBuffer): number {
  let value = readVarint32(bb);

  // ref: src/google/protobuf/wire_format_lite.h
  return (value >>> 1) ^ -(value & 1);
}

function writeVarint32ZigZag(bb: ByteBuffer, value: number): void {
  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint32(bb, (value << 1) ^ (value >> 31));
}

function readVarint64ZigZag(bb: ByteBuffer): Long {
  let value = readVarint64(bb, /* unsigned */ false);
  let low = value.low;
  let high = value.high;
  let flip = -(low & 1);

  // ref: src/google/protobuf/wire_format_lite.h
  return {
    low: ((low >>> 1) | (high << 31)) ^ flip,
    high: (high >>> 1) ^ flip,
    unsigned: false,
  };
}

function writeVarint64ZigZag(bb: ByteBuffer, value: Long): void {
  let low = value.low;
  let high = value.high;
  let flip = high >> 31;

  // ref: src/google/protobuf/wire_format_lite.h
  writeVarint64(bb, {
    low: (low << 1) ^ flip,
    high: ((high << 1) | (low >>> 31)) ^ flip,
    unsigned: false,
  });
}
