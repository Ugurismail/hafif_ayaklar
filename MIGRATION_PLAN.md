# QuestionRelationship Migration Planı

## Sorun
Django M2M field'a through eklenemez, AlterField ile.

## Çözüm: 3 Aşamalı Migration

### Migration 1: Geçici field ekle (subquestions_new)
1. QuestionRelationship modelini oluştur
2. Question.subquestions_new = M2M with through ekle
3. Eski subquestions → subquestions_new'e veri taşı

### Migration 2: Eski field'ı sil, yeni field'ı rename et
1. subquestions field'ını SİL
2. subquestions_new → subquestions RENAME

## DİKKAT
Bu işlem büyük ve riskli. Test ortamında denemeliyiz!

Alternatif: Daha basit yol var mı?
