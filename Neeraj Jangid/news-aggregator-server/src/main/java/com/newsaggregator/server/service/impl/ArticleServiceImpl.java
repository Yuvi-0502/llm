package com.newsaggregator.server.service.impl;

import com.newsaggregator.server.model.Article;
import com.newsaggregator.server.model.Category;
import com.newsaggregator.server.repository.ArticleRepository;
import com.newsaggregator.server.service.ArticleService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class ArticleServiceImpl implements ArticleService {

    private final ArticleRepository articleRepository;

    @Override
    public Article saveArticle(Article article) {
        return articleRepository.save(article);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Article> getArticleById(Long id) {
        return articleRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Article> getArticlesByCategory(Category category, Pageable pageable) {
        return articleRepository.findByCategory(category, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Article> getArticlesByDateRange(LocalDateTime start, LocalDateTime end, Pageable pageable) {
        return articleRepository.findByPublishedAtBetween(start, end, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Article> getArticlesByDateRangeAndCategory(LocalDateTime start, LocalDateTime end, Category category, Pageable pageable) {
        return articleRepository.findByPublishedAtBetweenAndCategory(start, end, category, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Article> searchArticles(String query, Pageable pageable) {
        return articleRepository.searchArticles(query, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Article> searchArticlesWithDateRange(String query, LocalDateTime start, LocalDateTime end, Pageable pageable) {
        return articleRepository.searchArticlesWithDateRange(query, start, end, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Article> getArticlesBySource(String source) {
        return articleRepository.findBySource(source);
    }

    @Override
    public void deleteArticle(Long id) {
        if (!articleRepository.existsById(id)) {
            throw new IllegalArgumentException("Article not found with id: " + id);
        }
        articleRepository.deleteById(id);
    }

    @Override
    public void updateArticle(Article article) {
        if (!articleRepository.existsById(article.getId())) {
            throw new IllegalArgumentException("Article not found with id: " + article.getId());
        }
        articleRepository.save(article);
    }

    @Override
    public void incrementLikes(Long articleId) {
        Article article = articleRepository.findById(articleId)
                .orElseThrow(() -> new IllegalArgumentException("Article not found with id: " + articleId));
        article.setLikesCount(article.getLikesCount() + 1);
        articleRepository.save(article);
    }

    @Override
    public void incrementDislikes(Long articleId) {
        Article article = articleRepository.findById(articleId)
                .orElseThrow(() -> new IllegalArgumentException("Article not found with id: " + articleId));
        article.setDislikesCount(article.getDislikesCount() + 1);
        articleRepository.save(article);
    }
} 