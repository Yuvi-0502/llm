package com.newsaggregator.server.controller;

import com.newsaggregator.server.dto.article.ArticleDTO;
import com.newsaggregator.server.dto.article.ArticleRequest;
import com.newsaggregator.server.mapper.ArticleMapper;
import com.newsaggregator.server.model.Article;
import com.newsaggregator.server.model.Category;
import com.newsaggregator.server.model.User;
import com.newsaggregator.server.service.ArticleService;
import com.newsaggregator.server.service.CategoryService;
import com.newsaggregator.server.service.SavedArticleService;
import com.newsaggregator.server.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/articles")
@RequiredArgsConstructor
public class ArticleController {

    private final ArticleService articleService;
    private final CategoryService categoryService;
    private final UserService userService;
    private final SavedArticleService savedArticleService;
    private final ArticleMapper articleMapper;

    @GetMapping("/public")
    public ResponseEntity<Page<ArticleDTO>> getPublicArticles(Pageable pageable) {
        Page<Article> articles = articleService.getArticlesByDateRange(
                LocalDateTime.now().minusDays(1), LocalDateTime.now(), pageable);
        return ResponseEntity.ok(articles.map(articleMapper::toDTO));
    }

    @GetMapping("/category/{categoryName}")
    public ResponseEntity<Page<ArticleDTO>> getArticlesByCategory(
            @PathVariable String categoryName,
            Pageable pageable) {
        Category category = categoryService.getCategoryByName(categoryName)
                .orElseThrow(() -> new IllegalArgumentException("Category not found"));
        Page<Article> articles = articleService.getArticlesByCategory(category, pageable);
        return ResponseEntity.ok(articles.map(articleMapper::toDTO));
    }

    @GetMapping("/search")
    public ResponseEntity<Page<ArticleDTO>> searchArticles(
            @RequestParam String query,
            @RequestParam(required = false) LocalDateTime start,
            @RequestParam(required = false) LocalDateTime end,
            Pageable pageable) {
        Page<Article> articles;
        if (start != null && end != null) {
            articles = articleService.searchArticlesWithDateRange(query, start, end, pageable);
        } else {
            articles = articleService.searchArticles(query, pageable);
        }
        return ResponseEntity.ok(articles.map(articleMapper::toDTO));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ArticleDTO> createArticle(@Valid @RequestBody ArticleRequest request) {
        Article article = articleMapper.toEntity(request);
        if (request.getCategoryName() != null) {
            Category category = categoryService.getCategoryByName(request.getCategoryName())
                    .orElseThrow(() -> new IllegalArgumentException("Category not found"));
            article.setCategory(category);
        }
        Article savedArticle = articleService.saveArticle(article);
        return ResponseEntity.ok(articleMapper.toDTO(savedArticle));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ArticleDTO> updateArticle(
            @PathVariable Long id,
            @Valid @RequestBody ArticleRequest request) {
        Article article = articleService.getArticleById(id)
                .orElseThrow(() -> new IllegalArgumentException("Article not found"));
        articleMapper.updateEntityFromRequest(request, article);
        if (request.getCategoryName() != null) {
            Category category = categoryService.getCategoryByName(request.getCategoryName())
                    .orElseThrow(() -> new IllegalArgumentException("Category not found"));
            article.setCategory(category);
        }
        Article updatedArticle = articleService.saveArticle(article);
        return ResponseEntity.ok(articleMapper.toDTO(updatedArticle));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> deleteArticle(@PathVariable Long id) {
        articleService.deleteArticle(id);
        return ResponseEntity.ok().build();
    }

    @PostMapping("/{id}/like")
    public ResponseEntity<?> likeArticle(@PathVariable Long id) {
        articleService.incrementLikes(id);
        return ResponseEntity.ok().build();
    }

    @PostMapping("/{id}/dislike")
    public ResponseEntity<?> dislikeArticle(@PathVariable Long id) {
        articleService.incrementDislikes(id);
        return ResponseEntity.ok().build();
    }

    @PostMapping("/{id}/save")
    public ResponseEntity<?> saveArticle(
            @PathVariable Long id,
            @AuthenticationPrincipal User user) {
        Article article = articleService.getArticleById(id)
                .orElseThrow(() -> new IllegalArgumentException("Article not found"));
        savedArticleService.saveArticle(new SavedArticle(null, user, article, null));
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/{id}/save")
    public ResponseEntity<?> unsaveArticle(
            @PathVariable Long id,
            @AuthenticationPrincipal User user) {
        savedArticleService.deleteSavedArticle(user, id);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/saved")
    public ResponseEntity<Page<ArticleDTO>> getSavedArticles(
            @AuthenticationPrincipal User user,
            Pageable pageable) {
        Page<SavedArticle> savedArticles = savedArticleService.getSavedArticlesByUser(user, pageable);
        return ResponseEntity.ok(savedArticles.map(savedArticle -> articleMapper.toDTO(savedArticle.getArticle())));
    }
} 