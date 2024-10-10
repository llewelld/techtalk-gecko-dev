/////////////////////////////////////////////////////////////////////////
// gecko-dev/gecko-dev/toolkit/components/windowwatcher/nsIPromptFactory.idl

/**
 * This interface allows creating various prompts that have a specific parent.
 */
[scriptable, uuid(2803541c-c96a-4ff1-bd7c-9cb566d46aeb)]
interface nsIPromptFactory : nsISupports
{
  /**
   * Returns an object implementing the specified interface that creates
   * prompts parented to aParent.
   */
  void getPrompt(in mozIDOMWindowProxy aParent, in nsIIDRef iid,
                 [iid_is(iid),retval] out nsQIResult result);
};

/////////////////////////////////////////////////////////////////////////
// embedlite-components/jscomps/LoginManagerPrompter.js

function LoginManagerPromptFactory() {
  Services.obs.addObserver(this, 
    "quit-application-granted", true);
  ...
}

LoginManagerPromptFactory.prototype = {
  classID : Components.ID("{72de694e-6c88-11e2-a4ee-...}"),
  QueryInterface: ChromeUtils.generateQI([
    Ci.nsIPromptFactory,
    Ci.nsIObserver,
    Ci.nsISupportsWeakReference,
  ]),

  observe : function (subject, topic, data) {
    if (topic == "quit-application-granted") {
      this._cancelPendingPrompts();
      ...
    }
  },

  getPrompt : function (aWindow, aIID) {
    var prompt = new LoginManagerPrompter()
                       .QueryInterface(aIID);
    prompt.init(aWindow, this);
    return prompt;
  },
  ...
}; // end of LoginManagerPromptFactory implementation


/////////////////////////////////////////////////////////////////////////
// gecko-dev/gecko-dev/toolkit/components/windowwatcher/nsWindowWatcher.cpp

NS_IMETHODIMP
nsWindowWatcher::GetNewPrompter(mozIDOMWindowProxy* aParent,
                                nsIPrompt** aResult) {
  // This is for backwards compat only. Callers should just use the prompt
  // service directly.
  nsresult rv;
  nsCOMPtr<nsIPromptFactory> factory =
      do_GetService("@mozilla.org/prompter;1", &rv);
  NS_ENSURE_SUCCESS(rv, rv);
  return factory->GetPrompt(aParent, NS_GET_IID(nsIPrompt),
                            reinterpret_cast<void**>(aResult));
}

/////////////////////////////////////////////////////////////////////////
// gecko-dev/gecko-dev/toolkit/components/prompts/src/Prompter.jsm

getPrompt(domWin, iid) {
  if (iid.equals(Ci.nsIAuthPrompt2) || iid.equals(Ci.nsIAuthPrompt)) {
    try {
      let pwmgr = Cc[
        "@mozilla.org/passwordmanager/authpromptfactory;1"
      ].getService(Ci.nsIPromptFactory);
      return pwmgr.getPrompt(domWin, iid);
    } catch (e) {
      Cu.reportError(
        "nsPrompter: Delegation to password manager failed: " + e
      );
    }
  }
},

/////////////////////////////////////////////////////////////////////////
// embedlite-components/jscomps/PromptService.js

if (iid.equals(Ci.nsIAuthPrompt2) || iid.equals(Ci.nsIAuthPrompt)) {
  try {
    let pwmgr = Cc["@mozilla.org/passwordmanager/authpromptfactory;1"].getService(Ci.nsIPromptFactory);
    return pwmgr.getPrompt(domWin, iid);
  } catch (e) {
    Cu.reportError("nsPrompter: Delegation to password manager failed: " + e);
  }
}

/////////////////////////////////////////////////////////////////////////
// https://searchfox.org/mozilla-central/source/__GENERATED__/dist/include/nsIPromptFactory.h
// gecko-dev/__GENERATED__/dist/include/nsPromptFactory.h

class NS_NO_VTABLE nsIPromptFactory : public nsISupports {
 public:

  NS_DECLARE_STATIC_IID_ACCESSOR(NS_IPROMPTFACTORY_IID)

  /* Used by ToJSValue to check which scriptable interface is implemented. */
  using ScriptableInterfaceType = nsIPromptFactory;

  /* void getPrompt (in mozIDOMWindowProxy aParent, in nsIIDRef iid, [iid_is (iid), retval] out nsQIResult result); */
  JS_HAZ_CAN_RUN_SCRIPT NS_IMETHOD GetPrompt(mozIDOMWindowProxy *aParent, const nsIID & iid, void * * result) = 0;

};

/////////////////////////////////////////////////////////////////////////
// https://searchfox.org/mozilla-central/source/__GENERATED__/dist/include/nsIPromptFactory.h
// Hand written C++ implementation of the interface

nsresult nsPromptFactory::Init() {
  AddObserver(this, "quit-application-granted", true);
  ...
}

NS_IMETHODIMP
nsPromptFactory::Observe(nsISupports* subject,
                   const char* topic, const char16_t* data) {
  if (!strcmp(topic, "quit-application-granted")) {
    this.CancelPendingPrompts();
    ...
  }

  return NS_OK;
}

NS_IMETHODIMP
nsPromptFactory::GetPrompt(mozIDOMWindowProxy *aParent,
                        const nsIID & iid, void * * result) {
  nsCOMPtr<nsISupports> login = new LoginManagerPrompter();
  nsCOMPtr<nsILoginManagerPrompter> prompt = login
                                .QueryInterface(iid, prompt);
  if (prompt) {
    prompt.Init(aParent, this);
  }

  *aResult = prompt.forget().take();
  return NS_OK;
}


