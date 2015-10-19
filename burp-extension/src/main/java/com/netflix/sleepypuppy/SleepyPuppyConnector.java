package com.netflix.sleepypuppy;

import burp.IBurpExtenderCallbacks;
import com.netflix.sleepypuppy.mapper.SleepyPuppyJsonMapper;
import com.netflix.sleepypuppy.model.SleepyPuppyAccessLog;
import com.netflix.sleepypuppy.model.SleepyPuppyAssessment;
import com.netflix.sleepypuppy.model.SleepyPuppyCapture;
import com.netflix.sleepypuppy.model.SleepyPuppyGenericCollector;
import com.netflix.sleepypuppy.util.SleepyPuppyHttpUtil;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by rperam on 10/2/15.
 */
public class SleepyPuppyConnector {

    private final IBurpExtenderCallbacks callbacks;
    private final PrintWriter stderr;
    private final SleepyPuppyData sleepyPuppyData = new SleepyPuppyData();
    private boolean connectionSuccess = false;

    public SleepyPuppyConnector(IBurpExtenderCallbacks callbacks) {
        this.callbacks = callbacks;
        this.stderr = new PrintWriter(callbacks.getStderr(), true);
    }

    public SleepyPuppyData getSleepyPuppyData() {
        return sleepyPuppyData;
    }

    public void refreshDataElements(JComboBox assessmentList, JComboBox payloadList, JLabel accessLogCountLabel,
                                    JLabel captureCountLabel, JLabel genericCollectorCountLabel) {
        if (connectionSuccess && (assessmentList.getSelectedIndex() > -1)) {
            refreshPayloadList(assessmentList, payloadList);
            refreshAccessLogList(assessmentList, accessLogCountLabel);
            refreshCaptureList(assessmentList, captureCountLabel);
            refreshGenericCollectorList(assessmentList, genericCollectorCountLabel);
        }
    }

    public void refreshAssessmentList(JComboBox assessmentList) {
        if (connectionSuccess) {
            // fetch Assessment list from Sleepy Puppy
            String assessments = SleepyPuppyHttpUtil.sendGetRequest(stderr,
                    sleepyPuppyData.getSleepyPuppyServerUrl() + SleepyPuppyConstants.ASSESSMENT_URL,
                    sleepyPuppyData.getSleepyPuppyUserApiKey());

            // parse assessment list and load them in to SleepyPuppyData instance
            parseAssessments(assessments);

            // refresh assessment list
            assessmentList.removeAllItems();
            Map<String, String> assessmentMapInner = sleepyPuppyData.getSleepyPuppyAssessments();
            if (assessmentMapInner != null && assessmentMapInner.size() > 0) {
                String[] assessmentNames = assessmentMapInner.values().toArray(new String[assessmentMapInner.size()]);
                for (String assessmentName : assessmentNames) {
                    assessmentList.addItem(assessmentName);
                }
            } else {
                stderr.println("Unable to fetch Assessment list from Sleepy Puppy Server");
            }
        }
    }

    private void refreshPayloadList(JComboBox assessmentList, JComboBox payloadList) {
        String selectedAssessmentName = (String) assessmentList.getSelectedItem();
        if (selectedAssessmentName != null && !selectedAssessmentName.isEmpty()) {
            Map<String, String> sleepyPuppyAssessments = sleepyPuppyData.getSleepyPuppyAssessments();
            if (sleepyPuppyAssessments != null && sleepyPuppyAssessments.size() > 0) {
                String selectedAssessmentId = null;
                for (Map.Entry<String, String> pair : sleepyPuppyAssessments.entrySet()) {
                    if (pair.getValue().equals(selectedAssessmentName)) {
                        selectedAssessmentId = pair.getKey();
                    }
                }
                if (selectedAssessmentId != null && !selectedAssessmentId.isEmpty()) {
                    // fetch payload list from Sleepy Puppy
                    String payloads = SleepyPuppyHttpUtil.sendGetRequest(stderr,
                            sleepyPuppyData.getSleepyPuppyServerUrl()
                                    + SleepyPuppyConstants.ASSESSMENT_PAYLOADS_URL
                                    + "/" + selectedAssessmentId,
                            sleepyPuppyData.getSleepyPuppyUserApiKey());

                    // parse payload list and load them in to SleepyPuppyData instance
                    parsePayloads(payloads);

                    // refresh payload list
                    payloadList.removeAllItems();
                    List<String> payloadNames = sleepyPuppyData.getSleepyPuppyAssessmentPayloads();
                    if (payloadNames != null && payloadNames.size() > 0) {
                        for (String payloadName : payloadNames) {
                            payloadList.addItem(payloadName);
                        }
                    }
                }
            } else {
                stderr.println("Unable to fetch payload list from Sleepy Puppy Server");
            }
        }
    }

    private void refreshAccessLogList(JComboBox assessmentList, JLabel accessLogCountLabel) {
        String selectedAssessmentName = (String) assessmentList.getSelectedItem();
        if (selectedAssessmentName != null && !selectedAssessmentName.isEmpty()) {
            // fetch access log list from Sleepy Puppy
            String accessLogs = SleepyPuppyHttpUtil.sendGetRequest(stderr,
                    sleepyPuppyData.getSleepyPuppyServerUrl()
                            + SleepyPuppyConstants.ACCESS_LOG_URL,
                    sleepyPuppyData.getSleepyPuppyUserApiKey());

            // parse payload list and load them in to SleepyPuppyData instance
            parseAccessLogs(accessLogs);

            Map<String, Integer> accessLogMap = sleepyPuppyData.getSleepyPuppyAccessLogCount();
            setLabel(accessLogMap, selectedAssessmentName, accessLogCountLabel, "Access Logs for Assessment");
        } else {
            stderr.println("Unable to fetch access log list from Sleepy Puppy Server");
        }
    }

    private void setLabel(Map<String, Integer> hashMap, String selectedAssessmentName, JLabel label,
                          String prefixText) {
        if (hashMap == null || selectedAssessmentName == null || label == null || prefixText == null) {
            return;
        }
        if (hashMap.get(selectedAssessmentName) != null) {
            label.setForeground(Color.RED);
            label.setText(prefixText + " (" + selectedAssessmentName + ") = "
                    + hashMap.get(selectedAssessmentName));
        } else {
            label.setForeground(Color.BLACK);
            label.setText(prefixText + " (" + selectedAssessmentName + ") = 0");
        }
    }

    private void refreshCaptureList(JComboBox assessmentList, JLabel captureCountLabel) {
        String selectedAssessmentName = (String) assessmentList.getSelectedItem();
        if (selectedAssessmentName != null && !selectedAssessmentName.isEmpty()) {
            // fetch access log list from Sleepy Puppy
            String captures = SleepyPuppyHttpUtil.sendGetRequest(stderr,
                    sleepyPuppyData.getSleepyPuppyServerUrl()
                            + SleepyPuppyConstants.CAPTURES_URL,
                    sleepyPuppyData.getSleepyPuppyUserApiKey());

            // parse payload list and load them in to SleepyPuppyData instance
            parseCaptures(captures);

            Map<String, Integer> captureMap = sleepyPuppyData.getSleepyPuppyCaptureCount();
            setLabel(captureMap, selectedAssessmentName, captureCountLabel, "Captures for Assessment");
        } else {
            stderr.println("Unable to fetch Captures from Sleepy Puppy Server");
        }
    }

    private void refreshGenericCollectorList(JComboBox assessmentList, JLabel genericCollectorCountLabel) {
        String selectedAssessmentName = (String) assessmentList.getSelectedItem();
        if (selectedAssessmentName != null && !selectedAssessmentName.isEmpty()) {
            // fetch access log list from Sleepy Puppy
            String genericCollectors = SleepyPuppyHttpUtil.sendGetRequest(stderr,
                    sleepyPuppyData.getSleepyPuppyServerUrl()
                            + SleepyPuppyConstants.GENERIC_COLLECTOR_URL,
                    sleepyPuppyData.getSleepyPuppyUserApiKey());

            // parse payload list and load them in to SleepyPuppyData instance
            parseGenericCollectors(genericCollectors);

            Map<String, Integer> genericCollectorMap = sleepyPuppyData.getSleepyPuppyGenericCollectorCount();
            setLabel(genericCollectorMap, selectedAssessmentName, genericCollectorCountLabel,
                    "Generic Collectors for Assessment");
        } else {
            stderr.println("Unable to fetch Generic Collector list from Sleepy Puppy Server");
        }
    }

    public void connectToSleepyPuppy(JLabel connectionResultLabel, String sleepyPuppyServerUrl,
                                     String sleepyPuppyUserApiKey) {
        if (sleepyPuppyServerUrl == null || sleepyPuppyServerUrl.equalsIgnoreCase("")) {
            stderr.println("Sleepy Puppy Server Location must be specified");
            return;
        }

        if (sleepyPuppyUserApiKey == null || sleepyPuppyUserApiKey.equalsIgnoreCase("")) {
            stderr.println("Sleepy Puppy API Key must be specified");
            return;
        }
        sleepyPuppyData.setSleepyPuppyServerUrl(sleepyPuppyServerUrl);
        sleepyPuppyData.setSleepyPuppyUserApiKey(sleepyPuppyUserApiKey);
        callbacks.saveExtensionSetting(SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_URL, sleepyPuppyServerUrl);
        callbacks.saveExtensionSetting(SleepyPuppyConstants.PROPERTY_SLEEPY_PUPPY_USER_API_KEY, sleepyPuppyUserApiKey);

        String assessments = SleepyPuppyHttpUtil.sendGetRequest(stderr, sleepyPuppyServerUrl
                + SleepyPuppyConstants.ASSESSMENT_URL,
                sleepyPuppyUserApiKey);
        if (assessments == null || assessments.isEmpty()) {
            connectionResultLabel.setForeground(Color.RED);
            connectionResultLabel.setText("Connection to Sleepy Puppy Failed");
            stderr.println("Unable to connect to Sleepy Puppy Server");
            connectionSuccess = false;
        } else {
            connectionResultLabel.setForeground(Color.GREEN);
            connectionResultLabel.setText("Connection to Sleepy Puppy Succeeded");
            connectionSuccess = true;

            parseAssessments(assessments);
        }
        Timer connectionResultConfirmationLabelTimer = new Timer(10000, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                connectionResultLabel.setText(null);
            }
        });
        connectionResultConfirmationLabelTimer.setRepeats(false);
        connectionResultConfirmationLabelTimer.start();
    }

    private void parseAssessments(String assessments) {
        if (!assessments.equals("{}")) {
            SleepyPuppyJsonMapper<SleepyPuppyAssessment[]> jsonMapper = new SleepyPuppyJsonMapper<>();
            SleepyPuppyAssessment[] sleepyPuppyAssessmentArray = jsonMapper.fromJson(stderr, assessments,
                    SleepyPuppyAssessment[].class);
            if (sleepyPuppyAssessmentArray != null) {
                Map<String, String> assessmentMap = new HashMap<>();
                for (SleepyPuppyAssessment assessment : sleepyPuppyAssessmentArray) {
                    assessmentMap.put(assessment.getId(), assessment.getName());
                }
                sleepyPuppyData.setSleepyPuppyAssessments(assessmentMap);
            } else {
                stderr.println("Unable to fetch Assessment list from Sleepy Puppy Server");
            }
        } else {
            stderr.println("Did not receive any Assessments from SleepyPuppy server. " +
                    "If you do not have any assessments on your server, you can start with creating a new Assessment");
            sleepyPuppyData.setSleepyPuppyAssessments(new HashMap<>());
        }
    }

    private void parsePayloads(String payloads) {
        if (!payloads.equals("{}")) {
            SleepyPuppyJsonMapper<String[]> jsonMapper = new SleepyPuppyJsonMapper<>();
            String[] sleepyPuppyPayloadArray = jsonMapper.fromJson(stderr, payloads, String[].class);
            if (sleepyPuppyPayloadArray != null) {
                List<String> payloadList = new ArrayList<>();
                for (int idx = sleepyPuppyPayloadArray.length - 1; idx >= 0; idx--) {
                    payloadList.add(sleepyPuppyPayloadArray[idx]);
                }

                sleepyPuppyData.setSleepyPuppyAssessmentPayloads(payloadList);
            } else {
                stderr.println("Unable to fetch payload list from Sleepy Puppy Server");
            }
        } else {
            stderr.println("Did not receive any payloads from SleepyPuppy server for the selected Assessment");
            sleepyPuppyData.setSleepyPuppyAssessmentPayloads(new ArrayList<>());
        }
    }

    private void parseAccessLogs(String accessLogs) {
        if (!accessLogs.equals("{}")) {
            SleepyPuppyJsonMapper<SleepyPuppyAccessLog[]> jsonMapper = new SleepyPuppyJsonMapper<>();
            SleepyPuppyAccessLog[] sleepyPuppyAccessLogArray = jsonMapper.fromJson(stderr, accessLogs,
                    SleepyPuppyAccessLog[].class);
            if (sleepyPuppyAccessLogArray != null) {
                sleepyPuppyData.setSleepyPuppyAccessLogCount(getAccessLogAssessmentCount(sleepyPuppyAccessLogArray));
            } else {
                stderr.println("Unable to fetch Access Log List from Sleepy Puppy Server");
            }
        } else {
            stderr.println("Did not receive any Access Logs from SleepyPuppy server for the selected Assessment");
            sleepyPuppyData.setSleepyPuppyAccessLogCount(new HashMap<>());
        }
    }

    private Map<String, Integer> getAccessLogAssessmentCount(SleepyPuppyAccessLog[] sleepyPuppyAccessLogArray) {
        Map<String, Integer> accessLogMap = new HashMap<>();
        for (SleepyPuppyAccessLog accessLog : sleepyPuppyAccessLogArray) {
            Integer count = accessLogMap.get(accessLog.getAssessment());
            accessLogMap.put(accessLog.getAssessment(), (count == null) ? 1 : count + 1);
        }
        return accessLogMap;
    }

    private void parseCaptures(String captures) {
        if (!captures.equals("{}")) {
            SleepyPuppyJsonMapper<SleepyPuppyCapture[]> jsonMapper = new SleepyPuppyJsonMapper<>();
            SleepyPuppyCapture[] sleepyPuppyCaptureArray = jsonMapper.fromJson(stderr, captures,
                    SleepyPuppyCapture[].class);
            if (sleepyPuppyCaptureArray != null) {
                sleepyPuppyData.setSleepyPuppyCaptureCount(getCaptureAssessmentCount(sleepyPuppyCaptureArray));
            } else {
                stderr.println("Unable to fetch Capture List from Sleepy Puppy Server");
            }
        } else {
            stderr.println("Did not receive any captures from SleepyPuppy server for the selected Assessment");
            sleepyPuppyData.setSleepyPuppyCaptureCount(new HashMap<>());
        }
    }

    private Map<String, Integer> getCaptureAssessmentCount(SleepyPuppyCapture[] sleepyPuppyCaptureArray) {
        Map<String, Integer> captureMap = new HashMap<>();
        for (SleepyPuppyCapture capture : sleepyPuppyCaptureArray) {
            Integer count = captureMap.get(capture.getAssessment());
            captureMap.put(capture.getAssessment(), (count == null) ? 1 : count + 1);
        }
        return captureMap;
    }

    private void parseGenericCollectors(String genericCollectors) {
        if (!genericCollectors.equals("{}")) {
            SleepyPuppyJsonMapper<SleepyPuppyGenericCollector[]> jsonMapper = new SleepyPuppyJsonMapper<>();
            SleepyPuppyGenericCollector[] sleepyPuppyGenericCollectorArray = jsonMapper.fromJson(stderr,
                    genericCollectors, SleepyPuppyGenericCollector[].class);
            if (sleepyPuppyGenericCollectorArray != null) {
                sleepyPuppyData.setSleepyPuppyGenericCollectorCount(getGenericCollectorAssessmentCount(
                        sleepyPuppyGenericCollectorArray));
            } else {
                stderr.println("Unable to fetch generic collector list from Sleepy Puppy Server");
            }
        } else {
            stderr.println("Did not receive any generic collectors from SleepyPuppy server for the selected Assessment");
            sleepyPuppyData.setSleepyPuppyGenericCollectorCount(new HashMap<>());
        }
    }

    private Map<String, Integer> getGenericCollectorAssessmentCount(
            SleepyPuppyGenericCollector[] sleepyPuppyGenericCollectorArray) {
        Map<String, Integer> genericCollectorMap = new HashMap<>();
        for (SleepyPuppyGenericCollector genericCollector : sleepyPuppyGenericCollectorArray) {
            Integer count = genericCollectorMap.get(genericCollector.getAssessment());
            genericCollectorMap.put(genericCollector.getAssessment(), (count == null) ? 1 : count + 1);
        }
        return genericCollectorMap;
    }

    public String createNewAssessment(String newAssessmentName) {
        return SleepyPuppyHttpUtil.sendPostRequestWithJsonPayload(stderr,
                sleepyPuppyData.getSleepyPuppyServerUrl() + SleepyPuppyConstants.ASSESSMENT_URL,
                "{\"name\": \"" + newAssessmentName + "\"}",
                sleepyPuppyData.getSleepyPuppyUserApiKey());
    }

    public String createNewPayload(String newPayloadValue) {
        return SleepyPuppyHttpUtil.sendPostRequestWithJsonPayload(stderr,
                sleepyPuppyData.getSleepyPuppyServerUrl() + SleepyPuppyConstants.PAYLOAD_URL,
                "{\"payload\": \"" + newPayloadValue
                        + "\", \"notes\": \"" + SleepyPuppyConstants.CREATE_PAYLOAD_NOTES + "\"}",
                sleepyPuppyData.getSleepyPuppyUserApiKey());
    }

    public List<String> getSleepyPuppyAssessmentPayloads() {
        return sleepyPuppyData.getSleepyPuppyAssessmentPayloads();
    }
}
