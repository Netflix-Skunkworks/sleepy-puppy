package com.netflix.sleepypuppy.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import javax.xml.bind.annotation.XmlRootElement;

/**
 * Created by rperam on 10/2/15.
 */
@XmlRootElement
public class SleepyPuppyGenericCollector {

    private int id;
    private String pub_date;
    private int payload;
    private String url;
    private String assessment;
    private String referrer;
    private String data;
    private String puppyscript_name;

    public SleepyPuppyGenericCollector() {
    }

    public SleepyPuppyGenericCollector(int id, String pub_date, int payload, String url, String assessment, String referrer, String data, String puppyscript_name) {
        this.id = id;
        this.pub_date = pub_date;
        this.payload = payload;
        this.url = url;
        this.assessment = assessment;
        this.referrer = referrer;
        this.data = data;
        this.puppyscript_name = puppyscript_name;
    }

    @JsonProperty("id")
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    @JsonProperty("pub_date")
    public String getPub_date() {
        return pub_date;
    }

    public void setPub_date(String pub_date) {
        this.pub_date = pub_date;
    }

    @JsonProperty("payload")
    public int getPayload() {
        return payload;
    }

    public void setPayload(int payload) {
        this.payload = payload;
    }

    @JsonProperty("url")
    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    @JsonProperty("assessment")
    public String getAssessment() {
        return assessment;
    }

    public void setAssessment(String assessment) {
        this.assessment = assessment;
    }

    @JsonProperty("referrer")
    public String getReferrer() {
        return referrer;
    }

    public void setReferrer(String referrer) {
        this.referrer = referrer;
    }

    @JsonProperty("data")
    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    @JsonProperty("puppyscript_name")
    public String getPuppyscript_name() {
        return puppyscript_name;
    }

    public void setPuppyscript_name(String puppyscript_name) {
        this.puppyscript_name = puppyscript_name;
    }
}
