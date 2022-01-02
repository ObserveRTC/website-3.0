---
contributors: {'Pallab', 'Balazs Kreith'}
title: "mediasoup client integration"
date: 2021-03-27 12:27:18
lastmod: 2021-05-30 19:37:44
draft: false
images: []
menu:
  docs:
    parent: "client-integration"
weight: 1030
toc: true
---

## mediasoup Integration

You can either [build and integrate the package yourself](https://github.com/ObserveRTC/integrations/wiki/Prepare-the-integration-library)
or use our [Mediasoup QuickStart](#quickstart) where you simply load the observer
libraries from GitHub's CDN and initialize by populating the `observerWsEndPoint` global variable using the
`ObserverRTC.ParserUtil.parseWsServerUrl` helper function.

See the quickstart methodology below for adding this library to your web app.


### mediasoup Quickstart <a name="quickstart"></a>

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
