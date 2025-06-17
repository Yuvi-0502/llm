package com.newsaggregator.server.service;

import com.newsaggregator.server.model.SavedArticle;
import com.newsaggregator.server.model.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface SavedArticleService {
    SavedArticle saveArticle(SavedArticle savedArticle);
    Page<SavedArticle> getSavedArticlesByUser(User user, Pageable pageable);
    void deleteSavedArticle(User user, Long articleId);
    boolean isArticleSavedByUser(User user, Long articleId);
} 