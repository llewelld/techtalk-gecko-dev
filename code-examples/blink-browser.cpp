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
  void PrintToPDF(const CefString& path,
                  const CefPdfPrintSettings& settings,
                  CefRefPtr<CefPdfPrintCallback> callback);
  void Find(const CefString& searchText,
                    bool forward,
                    bool matchCase,
                    bool findNext);
  void StopFinding(bool clearSelection);
  bool IsFullscreen();
  void ExitFullscreen(bool will_cause_resize);
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
};

