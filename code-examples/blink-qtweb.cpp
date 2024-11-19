class QWebEnginePage : public QObject
{
    Q_PROPERTY(QUrl requestedUrl...)
    Q_PROPERTY(qreal zoomFactor...)
    Q_PROPERTY(QString title..)
    Q_PROPERTY(QUrl url READ...)
    Q_PROPERTY(bool loading...)
    ...

public:
    explicit QWebEnginePage(QObject *parent);

    virtual void triggerAction(WebAction action,             bool checked);

    void findText(const QString &subString,                  FindFlags options, const std::function<void(const QWebEngineFindTextResult &)> &resultCallback);
    void load(const QUrl &url);
    void download(const QUrl &url, const QString &filename);
    void runJavaScript(const QString &scriptSource,          const std::function<void(const QVariant &)> &resultCallback);
    void fullScreenRequested(QWebEngineFullScreenRequest fullScreenRequest);
    ...
};

class QWebEngineView : public QWidget
{
    Q_PROPERTY(QString title...)
    Q_PROPERTY(QUrl url...)
    Q_PROPERTY(QString selectedText...)
    Q_PROPERTY(bool hasSelection...)
    Q_PROPERTY(qreal zoomFactor...)
    ...

public:
    explicit QWebEngineView(QWidget *parent);
    QWebEnginePage *page() const;
    void setPage(QWebEnginePage *page);

    void load(const QUrl &url);
    void findText(const QString &subString,                  FindFlags options, const std::function<void(const QWebEngineFindTextResult &)> &resultCallback);
    QWebEngineSettings *settings() const;
    void printToPdf(const QString &filePath, const QPageLayout &layout, const QPageRanges &ranges);
    ...

public slots:
    void stop();
    void back();
    void forward();
    void reload();
    ...
};
