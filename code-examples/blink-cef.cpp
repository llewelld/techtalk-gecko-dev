class CefBrowserHost : public CefBaseRefCounted {
 public:
  static bool CreateBrowser(const CefWindowInfo& windowInfo,
               CefRefPtr<CefClient> client,
               const CefString& url,
               const CefBrowserSettings& settings,
               CefRefPtr<CefDictionaryValue> extra_info,
               CefRefPtr<CefRequestContext> request_context);
  CefRefPtr<CefBrowser> GetBrowser();
  void CloseBrowser(bool force_close);
  ...
  void StartDownload(const CefString& url);
  ...
};

class CefFrame : public CefBaseRefCounted {
 public:
  CefRefPtr<CefBrowser> GetBrowser();
  void LoadURL(const CefString& url);
  CefString GetURL();
  CefString GetName();
  void Cut();
  void Copy();
  void Paste();
  void ExecuteJavaScript(const CefString& code,
                         const CefString& script_url,
                         int start_line);
  void SendProcessMessage(CefProcessId target_process,
                       CefRefPtr<CefProcessMessage> message);
  ...
};

class CefBrowser : public CefBaseRefCounted {
 public:
  bool CanGoBack();
  void GoBack();
  bool CanGoForward();
  void GoForward();
  bool IsLoading();
  void Reload();
  void StopLoad();
  bool HasDocument();
  CefRefPtr<CefFrame> GetMainFrame();
  ...
};

class CefV8Value : public virtual CefBaseRefCounted {
 public:
  static CefRefPtr<CefV8Value> CreateInt(int32_t value);
  bool IsInt();
  int32_t GetIntValue();
  static CefRefPtr<CefV8Value> CreateDouble(double value);
  ...

  static CefRefPtr<CefV8Value> CreateFunction(
    const CefString& name, CefRefPtr<CefV8Handler> handler);
  CefRefPtr<CefV8Value> ExecuteFunction(
      CefRefPtr<CefV8Value> object,
      const CefV8ValueList& arguments);
  ...
};
