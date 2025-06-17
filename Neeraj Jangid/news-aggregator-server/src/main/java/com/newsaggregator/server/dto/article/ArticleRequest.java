package com.newsaggregator.server.dto.article;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class ArticleRequest {
    @NotBlank
    private String title;

    private String description;
    private String content;

    @NotBlank
    private String source;

    @NotBlank
    private String url;

    private String imageUrl;
    private String categoryName;
} 