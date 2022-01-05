---
contributors: {'Pallab', 'Balazs Kreith'}
title: "Client Integrations"
date: 2021-03-27 12:27:18
lastmod: 2021-05-30 19:37:44
draft: false
images: []
menu:
  docs:
    parent: "overview"
weight: 1030
toc: true
---

## Janus Integration

You can either [build and integrate the package yourself](https://github.com/ObserveRTC/integrations/wiki/Prepare-the-integration-library)
or use our [Janus QuickStart](#quickstart) where you simply load the observer
libraries from GitHub's CDN and initialize by populating the `observerWsEndPoint` global variable using the
`ObserverRTC.ParserUtil.parseWsServerUrl` helper function.


### Tested plugins
  - video room plugin
  - audio bridge plugin

It should support other plugins as well out of the box. But, if you find some issue with it and if it does not fully support other plugins (s), please create an issue or pull request. Thanks

See the quickstart methodology below for adding this library to your web app.

### Janus Quickstart

1. Include core library before including janus javascript library file in your html page.
   We have a public version hosted on GitHub you can use as shown below,
   or use the library you built from the [build and integrate the package yourself](#build) instructions.

  - Production version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.min.js"></script>
    ```
  - Developer version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.js"></script>
    ```

2. Define server endpoint in global( window ) scope
    ```html
    <script>
        let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
            "wss://webrtc-observer.org/",           // observerURL
            {{ServiceUUID}},                        // Add a unique ServiceUUID here
            "janus-demo",                           // MediaUnitID
            "v20200114"                             // StatsVersion
        );
    </script>
    `````

3. Include the integration library

    You can also use the prebuilt libraries hosted on our GitHub links.
    We recommend the minified version. The unminified version includes extra console logging for debugging purposes.

    - Minified version (recommended):
    ```html
    <script src="https://observertc.github.io/integrations/dist/latest/janus.integration.min.js"></script>
    ```

    - OR Non-minified version:
    ```html
    <script src="https://observertc.github.io/integrations/dist/latest/janus.integration.js"></script>
    ```

    - In the end it might look similiar to this
        ```html
        <html>
        <body>
      <!--
      .....
      .....
      -->
        <script src="http://observertc.github.io/observer-js/dist/latest/observer.js"></script>
        <script>
            let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
                "ws://localhost:7080/",           // observerURL
                "b8bf0467-d7a9-4caa-93c9-8cd6e0dd7731", // Add a unique ServiceUUID here
                "janus-demo",                         // MediaUnitID
                "v20200114"                             // StatsVersion
            );
        </script>
        <script type="text/javascript" src="http://localhost:9090/dist/latest/janus.integration.js"></script>

        <script type="text/javascript" src="janus.js" ></script>
        <script type="text/javascript" src="videoroomtest.js"></script>

      ```


### 💎  **_Additional features in your integration_** 💎
* ➡️ [Tweak your integration](https://github.com/ObserveRTC/integrations/wiki/Tweak-your-integration)



## PeerJS Integration

You can either [build and integrate the package yourself](https://github.com/ObserveRTC/integrations/wiki/Prepare-the-integration-library)
or use our [PeerJS QuickStart](#quickstart) where you simply load the observer
libraries from GitHub's CDN and initialize by populating the `observerWsEndPoint` global variable using the
`ObserverRTC.ParserUtil.parseWsServerUrl` helper function.

See the quickstart methodology below for adding this library to your web app.

### PeerJS Quickstart

1. Include core library after peerjs javascript library file in your html page.
   We have a public version hosted on GitHub you can use as shown below,
   or use the library you built from the [build and integrate the package yourself](#build) instructions.

  - Production version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.min.js"></script>
    ```
  - Developer version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.js"></script>
    ```

2. Define server endpoint in global( window ) scope
    ```html
    <script>
        let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
            "wss://webrtc-observer.org/",           // observerURL
            {{ServiceUUID}},                        // Add a unique ServiceUUID here
            "peerjs-demo",                          // MediaUnitID
            "v20200114"                             // StatsVersion
        );
    </script>
    `````

3. Include the integration library

    You can also use the prebuilt libraries hosted on our GitHub links.
    We recommend the minified version. The unminified version includes extra console logging for debugging purposes.

    - Minified version (recommended):
    ```html
    <script src="https://observertc.github.io/integrations/dist/latest/peerjs.integration.min.js"></script>
    ```

    - OR Non-minified version:
    ```html
    <script src="https://observertc.github.io/integrations/dist/latest/peerjs.integration.js"></script>
    ```

    - In the end it might look similiar to this
        ```html
        <html>
        <body>
      <!--
      .....
      .....
      -->
        <script
            defer
            src="https://unpkg.com/peerjs@1.2.0/dist/peerjs.min.js"
        ></script>

        <script src="https://observertc.github.io/observer-js/dist/v2105-08/observer.js"></script>
        <script>
            let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
                "wss://webrtc-observer.org/",           // observerURL
                "uuidservice",                        // Add a unique ServiceUUID here
                "janus-demo",                           // MediaUnitID
                "v20200114"                             // StatsVersion
            );
        </script>
        <script defer src="https://observertc.github.io/integrations/dist/v2105-08/peerjs.integration.js"></script>

      ```


### 💎  **_Additional features in your integration_** 💎
* ➡️ [Tweak your integration](https://github.com/ObserveRTC/integrations/wiki/Tweak-your-integration)


## Mediasoup Integration

You can either [build and integrate the package yourself](https://github.com/ObserveRTC/integrations/wiki/Prepare-the-integration-library)
or use our [Mediasoup QuickStart](#quickstart) where you simply load the observer
libraries from GitHub's CDN and initialize by populating the `observerWsEndPoint` global variable using the
`ObserverRTC.ParserUtil.parseWsServerUrl` helper function.

See the quickstart methodology below for adding this library to your web app.


### Mediasoup Quickstart

1. Include core library before including `antiglobal.js` and mediasoup javascript library file in your html page.
   We have a public version hosted on GitHub you can use as shown below,
   or use the library you built from the [build and integrate the package yourself](#build) instructions.

  - Production version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.min.js"></script>
    ```
  - Developer version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.js"></script>
    ```

2. Define server endpoint in global( window ) scope
    ```html
    <script>
        let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
            "wss://webrtc-observer.org/",           // observerURL
            {{ServiceUUID}},                        // Add a unique ServiceUUID here
            "mediasoup-demo",                         // MediaUnitID
            "v20200114"                             // StatsVersion
        );
    </script>
    `````

3. Include the integration library

    You can also use the prebuilt libraries hosted on our GitHub links.
    We recommend the minified version. The unminified version includes extra console logging for debugging purposes.

    - Minified version (recommended):
    ```html
    <script src="https://observertc.github.io/integrations/dist/latest/mediasoup.integration.min.js"></script>
    ```

    - OR Non-minified version:
    ```html
    <script src="https://observertc.github.io/integrations/dist/latest/mediasoup.integration.js"></script>
    ```

    - In the end it might look similiar to this
        ```html
        <html>
        <body>
      <!--
      .....
      .....
      -->
        <script src="https://observertc.github.io/observer-js/dist/latest/observer.min.js"></script>
        <script>
            let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
                "ws://localhost:8088/",           // observerURL
                {{ServiceUUID}},                  // Add a unique ServiceUUID here
                "mediasoup-demo",                   // MediaUnitID
                "v20200114"                       // StatsVersion
            );
        </script>
        <script src='https://observertc.github.io/integrations/dist/v0.1.1/mediasoup.integration.min.js'></script>
        <script src='/resources/js/antiglobal.js'></script>
        <script>
        window.localStorage.setItem('debug', '* -engine* -socket* -RIE* *WARN* *ERROR*');

        if (window.antiglobal) {
            window.antiglobal('___browserSync___oldSocketIo', 'io', '___browserSync___', '__core-js_shared__');
            setInterval(window.antiglobal, 180000);
        }
        </script>
        <script async src='/mediasoup-demo-app.js?v=foo2'></script>

      ```


### 💎  **_Additional features in your integration_** 💎
* ➡️ [Tweak your integration](https://github.com/ObserveRTC/integrations/wiki/Tweak-your-integration)



## Vonage OpenTok Integration

You can either [build and integrate the package yourself](https://github.com/ObserveRTC/integrations/wiki/Prepare-the-integration-library)
or use our [OpenTok QuickStart](#quickstart) where you simply load the observer
libraries from GitHub's CDN and initialize by populating the `observerWsEndPoint` global variable using the
`ObserverRTC.ParserUtil.parseWsServerUrl` helper function.


See the quickstart methodology below for adding this library to your web app.

### OpenTok Quickstart

1. Include core library before including `opentok.js` file in your html page.
   We have a public version hosted on GitHub you can use as shown below,
   or use the library you built from the [build and integrate the package yourself](#opentok-build) instructions.

  - Production version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.min.js"></script>
    ```
  - Developer version
    ```html
    <script src="https://observertc.github.io/observer-js/dist/latest/observer.js"></script>
    ```

2. Define server endpoint in global( window ) scope
    ```html
    <script>
        let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
            "wss://webrtc-observer.org/",           // observerURL
            {{ServiceUUID}},                        // Add a unique ServiceUUID here
            "opentok-demo",                         // MediaUnitID
            "v20200114"                             // StatsVersion
        );
    </script>
    `````

3. Include the integration library

    You can also use the prebuilt libraries hosted on our GitHub links.
    We recommend the minified version. The unminified version includes extra console logging for debugging purposes.

    - Minified version (recommended):
    ```html
    <script src="https://observertc.github.io/integrations/dist/v0.1.1/tokbox.integration.min.js"></script>
    ```

    - OR Non-minified version:
    ```html
    <script src="https://observertc.github.io/integrations/dist/v0.1.1/tokbox.integration.js"></script>
    ```

    - In the end it might look similiar to this
        ```html
        <html>
        <body>
      <!--
      .....
      .....
      -->
        <script src="https://observertc.github.io/observer-js/dist/latest/observer.min.js"></script>
        <script>
        let observerWsEndPoint = ObserverRTC.ParserUtil.parseWsServerUrl(
            "ws://localhost:8088/",           // observerURL
            "b8bf0467-d7a9-4caa-93c9-8cd6e0dd7731", // Add a unique ServiceUUID here
            "opentok-demo",                         // MediaUnitID
            "v20200114"                             // StatsVersion
        );
        </script>
        <script src="https://observertc.github.io/integrations/dist/v0.1.1/tokbox.integration.min.js"></script>
        <script src="https://static.opentok.com/v2/js/opentok.js" charset="utf-8"></script>
        ```

An example can be found in [OpenTok demo folder](../../__test__/tokbox/index.html).


### 💎  **_Additional features in your integration_** 💎
* ➡️ [Tweak your integration](https://github.com/ObserveRTC/integrations/wiki/Tweak-your-integration)

## Create your own Integration

Currently, we have a couple of integration(s). In addition to that, anyone can write their own integration with a couple of lines. The fundamental part of the integration is to use the [observer-js](https://github.com/ObserveRTC/observer-js) core library to do most of the heavy lifting.

The integration will mainly handle the different use cases of how you can collect
 - peer connection
 - useful configuration parameters
 - maybe additional functionalities
from your application.

## Write own integration

### Include observer-js library

Let's assume you have already imported the [observer-js](https://github.com/ObserveRTC/observer-js) library. List of available versions can be found here.
 - https://github.com/ObserveRTC/observer-js/releases

Also, you can directly include it in your HTML page from Github. We are currently serving all versions from github. Like this

```html
<script src="https://observertc.github.io/observer-js/dist/latest/observer.js"></script>
```

Once included, observer-js will be available as `ObserverRTC` and expose some useful utility methods
- `ObserverRTC.Builder` - A builder class that you can use to build an instance of observer-js
- `ObserverRTC.logger` - Yet another application logger that is using [loglevel](https://www.npmjs.com/package/loglevel) to log in  observer-js core library.
- `ObserverRTC.ParserUtil` - Helper function that you can use to construct the WebSocket sender endpoint.

### Know your application
The integration will be fairly simple. In order to do that
 - 🔹  You somehow need to collect or I will say get the reference your peer connection from your application. Everything else is optional. 👍   Some WebRTC applications expose all your active peer connections to the global scope, some simply do not.
 - You might also want to send a `marker` to mark this peer connection session. This is optional, and to know about it please [visit this page](https://github.com/ObserveRTC/integrations/wiki/Tweak-your-integration#add-a-marker-during-build-time)
 - You might also want to send a browser id to uniquely identity this RTC session. More about it [can be found here](https://github.com/ObserveRTC/integrations/wiki/Tweak-your-integration#provide-a-custom-browser-id).
 - You might have a call id and want to send it too. Image it as a room id in your conference call where everybody joins, or name of the other peer or a common identifier that both peers in a P2P knows. It is optional.
 - You might also want to send a useId if you wish. It can be a user display name, or an identifier by how you uniquely identify a users in your application. It is again also optional.

### Write the integration

- #### Create integration object

  ```javascript
    const builder = new ObserverRTC.Builder({
      poolingIntervalInMs: 1*1000,
      wsAddress: 'wss://URL-OF-THE-DEPLYED-OBSERVER/',
    })
    // optional - If we want to set a marker
    builder.withMarker('my customer marker')
    // optional - If we want to set a browser id.
    // More details about it - https://github.com/ObserveRTC/integrations/wiki/Tweak-your-integration#provide-a-custom-browser-id
    builder.withBrowserId('my custom browser id')
    // A simple name to your integration
    builder.withIntegration('General')
    const integration = builder.build()
  ```

- #### Add peer connection to the integration from your application
  - #### **Approach 1**. Get the peer connection manually

      - It assumes that you have full control of your application peer connection. So, as soon as you create the peer connection please pass it via
        `addPC` method
         ```javascript
         const pcObject = aMethodToGetMyNewlyCreatedPC()
         const callId = 'optional call id'
         const userId = 'optional user id'
         integration.addPC(pcObject, callId, userId)
         ```

  - #### **Approach 2**. Or, override the peer connection object and set a callback to fetch the peer connection reference
    - You can also override the `RTCPeerConnection`, and hook it so that `addPC` will be called as soon as a `RTCPeerConnection` is created.
    - In order to override the `RTCPeerConnection`, please make sure you are calling as soon as document/window load.

      ```javascript
      const overridePeerConnection = (callback) => {
        if (!window.RTCPeerConnection) return
        const oldRTCPeerConnection = window.RTCPeerConnection
        window.RTCPeerConnection = function() {
            const pc = new oldRTCPeerConnection(...arguments)
            callback(pc)
            return pc
        }
        for (const key of Object.keys(oldRTCPeerConnection)) {
            window.RTCPeerConnection[key] = oldRTCPeerConnection[key]
        }
        window.RTCPeerConnection.prototype = oldRTCPeerConnection.prototype
      }
      const pcCallback = (pcObject) => {
        const callId = 'optional call id'
        const userId = 'optional user id'
        integration.addPC(pcObject, callId, userId)
      }
      overridePeerConnection(pcCallback)
      ```


