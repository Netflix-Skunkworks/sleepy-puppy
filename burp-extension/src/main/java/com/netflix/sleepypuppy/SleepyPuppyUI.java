package com.netflix.sleepypuppy;

import burp.IBurpExtenderCallbacks;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Map;

/**
 * Created by rperam on 10/2/15.
 */
public class SleepyPuppyUI {

    private final JLabel sleepyPuppyServerLocation = new JLabel();
    private final JTextField sleepyPuppyServerLocationText = new JTextField();
    private final JLabel sleepyPuppyUserApiKey = new JLabel();
    private final JTextField sleepyPuppyUserApiKeyText = new JTextField();
    private final JButton sleepyPuppyConnection = new JButton();
    private final JLabel accessLogCountLabel = new JLabel();
    private final JLabel captureCountLabel = new JLabel();
    private final JLabel genericCollectorCountLabel = new JLabel();
    private final JComboBox assessmentList = new JComboBox();

    private final SleepyPuppyConnector sleepyPuppyConnector;

    public SleepyPuppyUI(IBurpExtenderCallbacks callbacks) {
        sleepyPuppyConnector = new SleepyPuppyConnector(callbacks);
    }

    public SleepyPuppyConnector getSleepyPuppyConnector() {
        return sleepyPuppyConnector;
    }

    public JPanel buildSinglePanel(IBurpExtenderCallbacks callbacks) {
        JPanel panel = new JPanel();
        JComboBox payloadList = new JComboBox();

        panel.setLayout(null);
        sleepyPuppyServerLocation.setText("Sleepy Puppy Server URL: ");
        callbacks.customizeUiComponent(sleepyPuppyServerLocation);
        sleepyPuppyServerLocation.setLocation(10, 10);
        sleepyPuppyServerLocation.setSize(300, 30);
        panel.add(sleepyPuppyServerLocation);

        if (callbacks.loadExtensionSetting(SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_URL) != null
                && !callbacks.loadExtensionSetting(SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_URL).isEmpty()) {
            sleepyPuppyServerLocationText.setText(callbacks.loadExtensionSetting(
                    SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_URL));
        }
        sleepyPuppyServerLocationText.setText(callbacks.loadExtensionSetting(
                SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_URL));
        callbacks.customizeUiComponent(sleepyPuppyServerLocationText);
        sleepyPuppyServerLocationText.setLocation(200, 10);
        sleepyPuppyServerLocationText.setSize(300, 30);
        panel.add(sleepyPuppyServerLocationText);

        sleepyPuppyUserApiKey.setText("API Key");
        callbacks.customizeUiComponent(sleepyPuppyUserApiKey);
        sleepyPuppyUserApiKey.setLocation(10, 50);
        sleepyPuppyUserApiKey.setSize(300, 30);
        panel.add(sleepyPuppyUserApiKey);

        if (callbacks.loadExtensionSetting(SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_USER_API_KEY) != null
                && !callbacks.loadExtensionSetting(SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_USER_API_KEY).isEmpty()) {
            sleepyPuppyUserApiKeyText.setText(callbacks.loadExtensionSetting(
                    SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_USER_API_KEY));
        }
        callbacks.customizeUiComponent(sleepyPuppyUserApiKeyText);
        sleepyPuppyUserApiKeyText.setLocation(200, 50);
        sleepyPuppyUserApiKeyText.setSize(300, 30);
        panel.add(sleepyPuppyUserApiKeyText);

        JLabel connectionResultLabel = new JLabel();
        callbacks.customizeUiComponent(connectionResultLabel);
        connectionResultLabel.setLocation(400, 90);
        connectionResultLabel.setSize(300, 30);
        panel.add(connectionResultLabel);

        sleepyPuppyConnection.setText("Fetch Assessments");
        sleepyPuppyConnector.connectToSleepyPuppy(connectionResultLabel, sleepyPuppyServerLocationText.getText(),
                sleepyPuppyUserApiKeyText.getText());
        sleepyPuppyConnection.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // Test the connection to sleepy puppy
                sleepyPuppyConnector.connectToSleepyPuppy(connectionResultLabel,
                        sleepyPuppyServerLocationText.getText(), sleepyPuppyUserApiKeyText.getText());
                sleepyPuppyConnector.refreshAssessmentList(assessmentList);
            }
        });
        callbacks.customizeUiComponent(sleepyPuppyConnection);
        sleepyPuppyConnection.setLocation(10, 90);
        sleepyPuppyConnection.setSize(300, 30);
        panel.add(sleepyPuppyConnection);

        JSeparator parametersPanelSeparator = new JSeparator(JSeparator.HORIZONTAL);
        callbacks.customizeUiComponent(parametersPanelSeparator);
        parametersPanelSeparator.setLocation(10, 125);
        parametersPanelSeparator.setSize(1000, 10);
        panel.add(parametersPanelSeparator);

        JLabel assessmentLabel = new JLabel("Pick an Assessment");
        callbacks.customizeUiComponent(assessmentLabel);
        assessmentLabel.setLocation(10, 140);
        assessmentLabel.setSize(300, 30);
        panel.add(assessmentLabel);

        Map<String, String> assessmentMap = sleepyPuppyConnector.getSleepyPuppyData().getSleepyPuppyAssessments();
        String[] assessmentNames = null;
        if (assessmentMap != null && assessmentMap.size() > 0) {
            assessmentNames = assessmentMap.values().toArray(new String[assessmentMap.size()]);
        }
        if (assessmentNames != null && assessmentNames.length > 0) {
            for (String assessmentName : assessmentNames) {
                assessmentList.addItem(assessmentName);
            }
        }
        callbacks.customizeUiComponent(assessmentList);
        assessmentList.setLocation(200, 140);
        assessmentList.setSize(300, 30);
        sleepyPuppyConnector.refreshDataElements(assessmentList, payloadList, accessLogCountLabel,
                captureCountLabel, genericCollectorCountLabel);
        assessmentList.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                sleepyPuppyConnector.refreshDataElements(assessmentList, payloadList, accessLogCountLabel,
                        captureCountLabel, genericCollectorCountLabel);
            }
        });
        panel.add(assessmentList);


        JLabel payloadLabel = new JLabel("Payload List");
        callbacks.customizeUiComponent(payloadLabel);
        payloadLabel.setLocation(10, 180);
        payloadLabel.setSize(300, 30);
        panel.add(payloadLabel);

        callbacks.customizeUiComponent(payloadList);
        payloadList.setLocation(200, 180);
        payloadList.setSize(300, 30);
        panel.add(payloadList);

        callbacks.customizeUiComponent(accessLogCountLabel);
        accessLogCountLabel.setLocation(10, 190);
        accessLogCountLabel.setSize(500, 100);
        panel.add(accessLogCountLabel);

        callbacks.customizeUiComponent(captureCountLabel);
        captureCountLabel.setLocation(10, 220);
        captureCountLabel.setSize(500, 100);
        panel.add(captureCountLabel);

        callbacks.customizeUiComponent(genericCollectorCountLabel);
        genericCollectorCountLabel.setLocation(10, 250);
        genericCollectorCountLabel.setSize(500, 100);
        panel.add(genericCollectorCountLabel);

        JSeparator updatePanelSeparator = new JSeparator(JSeparator.HORIZONTAL);
        callbacks.customizeUiComponent(updatePanelSeparator);
        updatePanelSeparator.setLocation(10, 320);
        updatePanelSeparator.setSize(1000, 10);
        panel.add(updatePanelSeparator);

        // create a new assessment
        JLabel newAssessmentLabel = new JLabel("New Assessment Name");
        callbacks.customizeUiComponent(newAssessmentLabel);
        newAssessmentLabel.setLocation(10, 340);
        newAssessmentLabel.setSize(300, 30);
        panel.add(newAssessmentLabel);

        JTextField newAssessmentName = new JTextField();
        callbacks.customizeUiComponent(newAssessmentName);
        newAssessmentName.setLocation(200, 340);
        newAssessmentName.setSize(300, 30);
        panel.add(newAssessmentName);

        // label to confirm the creation of a new assessment
        JLabel createAssessmentConfirmationLabel = new JLabel();
        callbacks.customizeUiComponent(createAssessmentConfirmationLabel);
        createAssessmentConfirmationLabel.setLocation(800, 340);
        createAssessmentConfirmationLabel.setSize(300, 30);
        panel.add(createAssessmentConfirmationLabel);

        JButton createAssessmentButton = new JButton("Create New Assessment");
        callbacks.customizeUiComponent(createAssessmentButton);
        createAssessmentButton.setLocation(550, 340);
        createAssessmentButton.setSize(200, 30);
        createAssessmentButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (newAssessmentName.getText() != null && !newAssessmentName.getText().isEmpty()) {
                    String newAssessmentResponse = sleepyPuppyConnector.createNewAssessment(
                            newAssessmentName.getText());
                    newAssessmentName.setText("");

                    setCreateLabel(newAssessmentResponse, newAssessmentName, createAssessmentConfirmationLabel,
                            "New Assessment Creation");
//                    if (newAssessmentResponse.contains(newAssessmentName.getText())) {
//                        createAssessmentConfirmationLabel.setForeground(Color.BLACK);
//                        createAssessmentConfirmationLabel.setText("New Assessment Creation Succeeded");
//                    } else {
//                        createAssessmentConfirmationLabel.setForeground(Color.RED);
//                        createAssessmentConfirmationLabel.setText("New Assessment Creation Failed");
//                    }
                    Timer createAssessmentConfirmationLabelTimer = new Timer(5000, new ActionListener() {
                        @Override
                        public void actionPerformed(ActionEvent e) {
                            createAssessmentConfirmationLabel.setText(null);
                        }
                    });
                    createAssessmentConfirmationLabelTimer.setRepeats(false);
                    createAssessmentConfirmationLabelTimer.start();
                    sleepyPuppyConnector.refreshAssessmentList(assessmentList);
                }
            }
        });
        panel.add(createAssessmentButton);


        // create a new payload
        JLabel newPayloadLabel = new JLabel("New Payload");
        callbacks.customizeUiComponent(newPayloadLabel);
        newPayloadLabel.setLocation(10, 380);
        newPayloadLabel.setSize(300, 30);
        panel.add(newPayloadLabel);

        JTextField newPayloadValue = new JTextField();
        callbacks.customizeUiComponent(newPayloadValue);
        newPayloadValue.setLocation(200, 380);
        newPayloadValue.setSize(300, 30);
        panel.add(newPayloadValue);

        // label to confirm the creation of a new payload
        JLabel createPayloadConfirmationLabel = new JLabel();
        callbacks.customizeUiComponent(createPayloadConfirmationLabel);
        createPayloadConfirmationLabel.setLocation(800, 380);
        createPayloadConfirmationLabel.setSize(300, 30);
        panel.add(createPayloadConfirmationLabel);

        JButton createPayloadButton = new JButton("Create New Payload");
        callbacks.customizeUiComponent(createPayloadButton);
        createPayloadButton.setLocation(550, 380);
        createPayloadButton.setSize(200, 30);
        createPayloadButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (newPayloadValue.getText() != null && !newPayloadValue.getText().isEmpty()) {
                    String newPayloadResponse = sleepyPuppyConnector.createNewPayload(newPayloadValue.getText());
                    newPayloadValue.setText("");

                    setCreateLabel(newPayloadResponse, newPayloadValue, createPayloadConfirmationLabel,
                            "New Payload Creation");
//                    if (newPayloadResponse.contains(newPayloadValue.getText())) {
//                        createPayloadConfirmationLabel.setForeground(Color.BLACK);
//                        createPayloadConfirmationLabel.setText("New Payload Creation Succeeded");
//                    } else {
//                        createPayloadConfirmationLabel.setForeground(Color.RED);
//                        createPayloadConfirmationLabel.setText("New Payload Creation Failed");
//                    }
                    Timer createPayloadConfirmationLabelTimer = new Timer(5000, new ActionListener() {
                        @Override
                        public void actionPerformed(ActionEvent e) {
                            createPayloadConfirmationLabel.setText(null);
                        }
                    });
                    createPayloadConfirmationLabelTimer.setRepeats(false);
                    createPayloadConfirmationLabelTimer.start();
                    sleepyPuppyConnector.refreshAssessmentList(assessmentList);
                }
            }
        });
        panel.add(createPayloadButton);

        JSeparator newPayloadSeparator = new JSeparator(JSeparator.HORIZONTAL);
        callbacks.customizeUiComponent(newPayloadSeparator);
        newPayloadSeparator.setLocation(10, 420);
        newPayloadSeparator.setSize(1000, 10);
        panel.add(newPayloadSeparator);

        return panel;
    }

    private void setCreateLabel(String response, JTextField textField,
                                JLabel label, String text) {
        if (response == null || textField == null || label == null || text == null) {
            return;
        }
        if (response.contains(textField.getText())) {
            label.setForeground(Color.BLACK);
            label.setText(text + " Succeeded");
        } else {
            label.setForeground(Color.RED);
            label.setText(" Failed");
        }
    }
}
