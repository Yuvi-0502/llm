package com.newsaggregator.server.service.impl;

import com.newsaggregator.server.model.SavedArticle;
import com.newsaggregator.server.model.User;
import com.newsaggregator.server.repository.SavedArticleRepository;
import com.newsaggregator.server.service.SavedArticleService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional
public class SavedArticleServiceImpl implements SavedArticleService {

    private final SavedArticleRepository savedArticleRepository;

    @Override
    public SavedArticle saveArticle(SavedArticle savedArticle) {
        if (savedArticleRepository.existsByUserAndArticleId(savedArticle.getUser(), savedArticle.getArticle().getId())) {
            throw new IllegalArgumentException("Article already saved by user");
        }
        return savedArticleRepository.save(savedArticle);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<SavedArticle> getSavedArticlesByUser(User user, Pageable pageable) {
        return savedArticleRepository.findByUser(user, pageable);
    }

    @Override
    public void deleteSavedArticle(User user, Long articleId) {
        if (!savedArticleRepository.existsByUserAndArticleId(user, articleId)) {
            throw new IllegalArgumentException("Saved article not found");
        }
        savedArticleRepository.deleteByUserAndArticleId(user, articleId);
    }

    @Override
    @Transactional(readOnly = true)
    public boolean isArticleSavedByUser(User user, Long articleId) {
        return savedArticleRepository.existsByUserAndArticleId(user, articleId);
    }
} 