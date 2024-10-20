/////////////////////////////////////////////////////////////////////////
// gecko-dev-esr91/gecko-dev/gecko-dev/js/public/Value.h
// JS::Value definition
// JIT assumes max 47 bit memory pointers
// See: https://bugzilla.mozilla.org/show_bug.cgi?id=1143022
// See: https://bugzilla.mozilla.org/show_bug.cgi?id=910845
// For punboxing see:
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number
// https://devdoc.net/web/developer.mozilla.org/en-US/docs/SpiderMonkey/Internals.1.html#JavaScript_values

#define JSVAL_TAG_SHIFT 47

class alignas(8) Value {
 private:
  uint64_t asBits_;

  static uint64_t bitsFromDouble(double d) {
    d = CanonicalizeNaN(d);
    return mozilla::BitwiseCast<uint64_t>(d);
  }

 public:
  static constexpr uint64_t bitsFromTagAndPayload(
    JSValueTag tag, uint64_t payload) {
    return (uint64_t(tag) << JSVAL_TAG_SHIFT) | payload;
  }
  ...

  /*** Value type queries ***/
  bool isUndefined() const {
    return asBits_ == JSVAL_SHIFTED_TAG_UNDEFINED;
  }

  bool isInt32() const {
    return toTag() == JSVAL_TAG_INT32;
  }

  bool isDouble() const {
    return ValueIsDouble(asBits_);
  }

  bool isString() const {
    return toTag() == JSVAL_TAG_STRING;
  }
  ...

  /*** Mutators ***/
  void setUndefined() {
    asBits_ = bitsFromTagAndPayload(JSVAL_TAG_UNDEFINED, 0);
  }

  void setInt32(int32_t i) {
    asBits_ = bitsFromTagAndPayload(
                              JSVAL_TAG_INT32, uint32_t(i));
  }

  void setDouble(double d) {
    asBits_ = bitsFromDouble(d);
  }

  void setString(JSString* str) {
    asBits_ = bitsFromTagAndPayload(
                           JSVAL_TAG_STRING, uint64_t(str));
  }
  ...

  /*** Extract the value's typed payload ***/
  int32_t toInt32() const {
    return int32_t(asBits_);
  }

  double toDouble() const {
    return mozilla::BitwiseCast<double>(asBits_);
  }

  JSString* toString() const {
    return unboxGCPointer<JSString, JSVAL_TAG_STRING>();
  }
  ...

} JS_HAZ_GC_POINTER MOZ_NON_PARAM;

