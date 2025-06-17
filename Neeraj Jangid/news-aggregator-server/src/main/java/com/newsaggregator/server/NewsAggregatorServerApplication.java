package com.newsaggregator.server;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class NewsAggregatorServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(NewsAggregatorServerApplication.class, args);
    }
} 