package com.netflix.sleepypuppy.mapper;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.io.PrintWriter;

/**
 * Created by rperam on 9/14/15.
 */
public class SleepyPuppyJsonMapper<T> {

    public String toJson(PrintWriter stderr, T t) {
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonString = null;
        try {
            jsonString = objectMapper.writeValueAsString(t);
        } catch (IOException e) {
            stderr.println("Failed to convert " + t + "to Json: " + e.getMessage());
        }
        return jsonString;
    }

    public T fromJson(PrintWriter stderr, String jsonStr, Class<T> clazz) {
        T t = null;
        if (jsonStr != null && !jsonStr.isEmpty()) {
            ObjectMapper mapper = new ObjectMapper();
            try {
                t = mapper.readValue(jsonStr, clazz);
            } catch (IOException e) {
                stderr.println("Failed to parse jsonStr: " + jsonStr + " : " + e.getMessage());
            }
        }
        return t;
    }
}
