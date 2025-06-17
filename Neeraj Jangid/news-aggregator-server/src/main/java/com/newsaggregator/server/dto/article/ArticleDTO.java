package com.newsaggregator.server.dto.article;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class ArticleDTO {
    private Long id;
    private String title;
    private String description;
    private String content;
    private String source;
    private String url;
    private String imageUrl;
    private LocalDateTime publishedAt;
    private String categoryName;
    private Integer likesCount;
    private Integer dislikesCount;
    private boolean saved;
} 