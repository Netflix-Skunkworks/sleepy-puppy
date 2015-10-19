package com.netflix.sleepypuppy;

import java.util.List;
import java.util.Map;

/**
 * Created by rperam on 9/14/15.
 */
public class SleepyPuppyData {

    private String sleepyPuppyServerUrl;
    private String sleepyPuppyUserApiKey;
    private Map<String, String> sleepyPuppyAssessments;
    private List<String> sleepyPuppyAssessmentPayloads;
    private Map<String, Integer> sleepyPuppyAccessLogCount;
    private Map<String, Integer> sleepyPuppyCaptureCount;
    private Map<String, Integer> sleepyPuppyGenericCollectorCount;


    public String getSleepyPuppyServerUrl() {
        return sleepyPuppyServerUrl;
    }

    public void setSleepyPuppyServerUrl(String sleepyPuppyServerUrl) {
        this.sleepyPuppyServerUrl = sleepyPuppyServerUrl;
    }

    public String getSleepyPuppyUserApiKey() {
        return sleepyPuppyUserApiKey;
    }

    public void setSleepyPuppyUserApiKey(String sleepyPuppyUserApiKey) {
        this.sleepyPuppyUserApiKey = sleepyPuppyUserApiKey;
    }


    public Map<String, String> getSleepyPuppyAssessments() {
        return sleepyPuppyAssessments;
    }

    public void setSleepyPuppyAssessments(Map<String, String> sleepyPuppyAssessments) {
        this.sleepyPuppyAssessments = sleepyPuppyAssessments;
    }

    public List<String> getSleepyPuppyAssessmentPayloads() {
        return sleepyPuppyAssessmentPayloads;
    }

    public void setSleepyPuppyAssessmentPayloads(List<String> sleepyPuppyAssessmentPayloads) {
        this.sleepyPuppyAssessmentPayloads = sleepyPuppyAssessmentPayloads;
    }

    public Map<String, Integer> getSleepyPuppyAccessLogCount() {
        return sleepyPuppyAccessLogCount;
    }

    public void setSleepyPuppyAccessLogCount(Map<String, Integer> sleepyPuppyAccessLogCount) {
        this.sleepyPuppyAccessLogCount = sleepyPuppyAccessLogCount;
    }

    public Map<String, Integer> getSleepyPuppyCaptureCount() {
        return sleepyPuppyCaptureCount;
    }

    public void setSleepyPuppyCaptureCount(Map<String, Integer> sleepyPuppyCaptureCount) {
        this.sleepyPuppyCaptureCount = sleepyPuppyCaptureCount;
    }

    public Map<String, Integer> getSleepyPuppyGenericCollectorCount() {
        return sleepyPuppyGenericCollectorCount;
    }

    public void setSleepyPuppyGenericCollectorCount(Map<String, Integer> sleepyPuppyGenericCollectorCount) {
        this.sleepyPuppyGenericCollectorCount = sleepyPuppyGenericCollectorCount;
    }
}
