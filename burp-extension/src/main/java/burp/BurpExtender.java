package burp;

import com.netflix.sleepypuppy.SleepyPuppyUI;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;


/**
 * Created by rperam on 9/8/15.
 */
public class BurpExtender implements IBurpExtender, IIntruderPayloadGeneratorFactory,
        IScannerCheck, ITab, IContextMenuFactory, ActionListener {

    private IBurpExtenderCallbacks callbacks;
    private JPanel mainPanel;

    private IContextMenuInvocation invocation;
    private IExtensionHelpers helpers;
    private SleepyPuppyUI sleepyPuppyUI;

    //
    // implement IBurpExtender
    //

    @Override
    public void registerExtenderCallbacks(final IBurpExtenderCallbacks callbacks) {
        // keep a reference to our callbacks object
        this.callbacks = callbacks;
        this.sleepyPuppyUI = new SleepyPuppyUI(callbacks);

        // obtain an extension helpers object
        helpers = callbacks.getHelpers();

        // set the extension name
        callbacks.setExtensionName("Sleepy Puppy Extension");

        // register as a context menu provider
        callbacks.registerContextMenuFactory(this);

        // register as a custom scanner check
        callbacks.registerScannerCheck(this);

        // register as an Intruder payload generator
        callbacks.registerIntruderPayloadGeneratorFactory(this);

        // create UI
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                mainPanel = sleepyPuppyUI.buildSinglePanel(callbacks);

                // customize our UI components
                callbacks.customizeUiComponent(mainPanel);

                // add the custom tab to Burp's UI
                callbacks.addSuiteTab(BurpExtender.this);
            }
        });
    }


    //
    // implement ITab
    //

    @Override
    public String getTabCaption() {
        return "Sleepy Puppy";
    }

    @Override
    public Component getUiComponent() {
        return mainPanel;
    }


    //
    // implement IScannerCheck
    //

    @Override
    public List<IScanIssue> doPassiveScan(IHttpRequestResponse baseRequestResponse) {
        // do nothing in passive scan
        return null;
    }

    @Override
    public List<IScanIssue> doActiveScan(IHttpRequestResponse baseRequestResponse,
                                         IScannerInsertionPoint insertionPoint) {
        List<String> payloads = getSleepyPuppyAssessmentPayloads();
        for (String payload : payloads) {
            byte[] payloadBytes = payload.getBytes();
            // make a request containing our injection test in the insertion point
            byte[] checkRequest = insertionPoint.buildRequest(payloadBytes);
            IHttpRequestResponse checkRequestResponse = callbacks.makeHttpRequest(
                    baseRequestResponse.getHttpService(), checkRequest);
            checkRequestResponse.getResponse();
        }
        // Sleepy Puppy will notify us if the XSS payload gets triggered
        // hence no need to check for response
        return null;
    }

    @Override
    public int consolidateDuplicateIssues(IScanIssue existingIssue, IScanIssue newIssue) {
        // no response check being done.
        // without any issues being identified, there is no need to deduplicate issues
        return 0;
    }


    //
    // implement IIntruderPayloadGeneratorFactory
    //

    @Override
    public String getGeneratorName() {
        return "Sleepy Puppy";
    }

    @Override
    public IIntruderPayloadGenerator createNewInstance(IIntruderAttack attack) {
        // return a new IIntruderPayloadGenerator to generate payloads for this attack
        return new IntruderPayloadGenerator();
    }

    //
    // class to generate payloads from a simple list
    //

    class IntruderPayloadGenerator implements IIntruderPayloadGenerator {
        int payloadIndex;

        @Override
        public boolean hasMorePayloads() {
            return payloadIndex < getSleepyPuppyAssessmentPayloads().size();
        }

        @Override
        public byte[] getNextPayload(byte[] baseValue) {
            byte[] payload = getSleepyPuppyAssessmentPayloads().get(payloadIndex).getBytes();
            payloadIndex++;

            return payload;
        }

        @Override
        public void reset() {
            payloadIndex = 0;
        }
    }

    //
    // implement IContextMenuFactory
    //

    @Override
    public ArrayList<JMenuItem> createMenuItems(IContextMenuInvocation invocation) {
        byte invocationContext = invocation.getInvocationContext();

        if (invocation.getToolFlag() == IBurpExtenderCallbacks.TOOL_REPEATER) {
            this.invocation = invocation;

            ArrayList<JMenuItem> menu = new ArrayList<>();
            if (invocationContext == IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_REQUEST
                    || invocationContext == IContextMenuInvocation.CONTEXT_MESSAGE_VIEWER_REQUEST) {
                JMenu main = new JMenu("Sleepy Puppy Payloads");
                menu.add(main);
                List<String> payloads = getSleepyPuppyAssessmentPayloads();
                for (String payload : payloads) {
                    JMenuItem item = new JMenuItem(payload);
                    item.addActionListener(this);
                    main.add(item);
                }
            }
            return menu;
        } else {
            return null;
        }
    }


    //
    // implement ActionListener
    //

    @Override
    public void actionPerformed(ActionEvent e) {
        int[] selectionBounds = invocation.getSelectionBounds();
        IHttpRequestResponse[] invocationSelectedMessages = invocation.getSelectedMessages();

        for (IHttpRequestResponse invocationSelectedMessage : invocationSelectedMessages) {
            IRequestInfo requestInfo = helpers.analyzeRequest(invocationSelectedMessage.getRequest());
            String request = new String(invocationSelectedMessage.getRequest());
            String modifiedRequest = "";
            // Do not encode the payload only if the payload is part of POST body
            // If payload is added as part of URL/headers of GET, POST, etc., encode the payload
            if (requestInfo.getMethod().equalsIgnoreCase("POST")) {
                if (selectionBounds[0] < requestInfo.getBodyOffset()) {
                    modifiedRequest = request.substring(0, selectionBounds[0]) + helpers.urlEncode(e.getActionCommand())
                            + request.substring(selectionBounds[1]);
                } else {
                    modifiedRequest = request.substring(0, selectionBounds[0]) + e.getActionCommand()
                            + request.substring(selectionBounds[1]);
                }
            } else {
                modifiedRequest = request.substring(0, selectionBounds[0]) + helpers.urlEncode(e.getActionCommand())
                        + request.substring(selectionBounds[1]);
            }

            invocationSelectedMessage.setRequest(modifiedRequest.getBytes());
        }
    }

    private List<String> getSleepyPuppyAssessmentPayloads() {
        return sleepyPuppyUI.getSleepyPuppyConnector().getSleepyPuppyAssessmentPayloads();
    }
}
