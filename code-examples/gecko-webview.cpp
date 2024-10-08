class WebEngine
{
public:
    static WebEngine *instance();
    ...

public slots:
    void addObserver(const QString &aTopic);
    void removeObserver(const QString &aTopic);
    void notifyObservers(const QString &topic, const QString &value);
    void addComponentManifest(const QString &manifestPath);
    void setProfile(const QString &);
    ...

public signals:
    void recvObserve(const QString message, const QVariant data);
    ...
};

class WebEngineSettings
{
    Q_PROPERTY(bool autoLoadImages...)
    Q_PROPERTY(bool javascriptEnabled...)
    Q_PROPERTY(bool popupEnabled...)
    Q_PROPERTY(CookieBehavior cookieBehavior...)
    ...

public:
    static WebEngineSettings *instance();
    ...
};

class QuickMozView : public QQuickItem
{
    Q_PROPERTY(QUrl url...)
    Q_PROPERTY(QString title...)
    Q_PROPERTY(bool canGoBack...)
    Q_PROPERTY(bool canGoForward...)
    Q_PROPERTY(int loadProgress...)
    Q_PROPERTY(QString httpUserAgent...)
    ...

public:
    void runJavaScript(const QString &script, const QJSValue &callback, const QJSValue &errorCallback);
    void load(const QString&, const bool& fromExternal);
    void reload();
    void stop();
    void goBack();
    void goForward();
    void loadHtml(const QString &html, const QUrl &baseUrl);
    ...
};

