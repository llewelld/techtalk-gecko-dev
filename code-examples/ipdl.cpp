/////////////////////////////////////////////////////////////////////////
// gecko-dev/embedding/embedlite/PEmbedLiteView.ipdl
// (hand-written)

nested(upto inside_sync) sync protocol PEmbedLiteView
{
child:
    async LoadURL(nsString url, bool aFromExternal);
    ...
parent:
    async OnLoadStarted(nsCString aLocation);
    ...
};

/////////////////////////////////////////////////////////////////////////
// gecko-dev/obj-build-mer-qt-xr/ipc/ipdl/_ipdlheaders/mozilla/embedlite/PEmbedLiteViewChild.h
// (generated)

class PEmbedLiteViewChild :
    public mozilla::ipc::IProtocol
{
    ...
public:
    bool
    SendOnLoadStarted(const nsCString& aLocation);
    ...
};

/////////////////////////////////////////////////////////////////////////
// gecko-dev/obj-build-mer-qt-xr/ipc/ipdl/_ipdlheaders/mozilla/embedlite/PEmbedLiteViewParent.h
// (generated)

class PEmbedLiteViewParent :
    public mozilla::ipc::IProtocol
{
    ...
public:
    [[nodiscard]] bool
    SendLoadURL(
            const nsString& url,
            const bool& aFromExternal);
    ...
};

/////////////////////////////////////////////////////////////////////////
// gecko-dev/embedding/embedlite/embedshared/EmbedLiteViewChild.h
// (hand-written)

class EmbedLiteViewChild :
    public PEmbedLiteViewChild
{
    ...
protected:
    virtual mozilla::ipc::IPCResult RecvLoadURL(
        const nsString &,
        const bool& aFromExternal
    );
    ...
};

/////////////////////////////////////////////////////////////////////////
// gecko-dev/embedding/embedlite/embedshared/EmbedLiteViewParent.h
// (hand-written)

class EmbedLiteViewParent :
    public PEmbedLiteViewParent
{
    ...
protected:
    virtual mozilla::ipc::IPCResult RecvOnLoadStarted(
        const nsCString &aLocation
    );
    ...
};

/////////////////////////////////////////////////////////////////////////
// gecko-dev/obj-build-mer-qt-xr/ipc/ipdl/PEmbedLiteViewParent.cpp
// (generated)

auto PEmbedLiteViewParent::OnMessageReceived(
  const Message& msg__) -> PEmbedLiteViewParent::Result
{
  switch (msg__.type()) {
  ...
  case PEmbedLiteView::Msg_OnLoadStarted__ID:
    {
      PickleIterator iter__{msg__};
      nsCString aLocation{};

      if ((!(ReadIPDLParam((&(msg__)), (&(iter__)), this, (&(aLocation)))))) {
        FatalError("Error deserializing 'nsCString'");
        return MsgValueError;
      }
      ...
      msg__.EndRead(iter__, msg__.type());
      if ((!((static_cast<EmbedLiteViewParent*>(this))->RecvOnLoadStarted(std::move(aLocation))))) {
        mozilla::ipc::ProtocolErrorBreakpoint("Handler returned error code!");
        // Error handled in mozilla::ipc::IPCResult
        return MsgProcessingError;
      }

      return MsgProcessed;
    }
  ...
  default:
    return MsgNotKnown;
  }
}


