package com.newsaggregator.server.service;

import com.newsaggregator.server.model.Article;
import com.newsaggregator.server.model.Category;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface ArticleService {
    Article saveArticle(Article article);
    Optional<Article> getArticleById(Long id);
    Page<Article> getArticlesByCategory(Category category, Pageable pageable);
    Page<Article> getArticlesByDateRange(LocalDateTime start, LocalDateTime end, Pageable pageable);
    Page<Article> getArticlesByDateRangeAndCategory(LocalDateTime start, LocalDateTime end, Category category, Pageable pageable);
    Page<Article> searchArticles(String query, Pageable pageable);
    Page<Article> searchArticlesWithDateRange(String query, LocalDateTime start, LocalDateTime end, Pageable pageable);
    List<Article> getArticlesBySource(String source);
    void deleteArticle(Long id);
    void updateArticle(Article article);
    void incrementLikes(Long articleId);
    void incrementDislikes(Long articleId);
} 