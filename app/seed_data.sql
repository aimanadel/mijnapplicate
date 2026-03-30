/* * Seed Data for Brain Boost
 * Purpose: Fills the 'exercises' and 'result' tables with initial data from the wireframe.
 */

-- Insert exercises for the "Recommended" section
INSERT INTO exercises (title, description, duration, question_count, color_code, status)
VALUES 
('Vermijd Haastige Conclusies', 'Leer alle antwoordopties grondig te lezen voordat je kiest.', 15, 12, '#D38D8D', 'recommended'),
('Sleutelwoorden Herkennen', 'Oefen met het markeren van belangrijke woorden zoals "NIET" en "ALLEEN".', 10, 8, '#8D8DB7', 'recommended'),
('Tijdsplanning Verbeteren', 'Oefen met tijdsbeheer tijdens toetsen en lastige vragen.', 20, 15, '#74A9CF', 'recommended');

-- Insert exercises for the "Soon" (Binnenkort) section
INSERT INTO exercises (title, description, status)
VALUES 
('Nauwkeurigheid Training', 'Coming soon: Focus op details.', 'upcoming'),
('Spelling & Grammatica', 'Coming soon: Verbeter je taalvaardigheid.', 'upcoming');

-- Insert some initial results for the sidebar
-- Note: exercise_id 1 refers to 'Vermijd Haastige Conclusies'
INSERT INTO result (exercise_id, score, completion_time)
VALUES 
(1, 8.5, '2026-03-28 14:30:00'),
(2, 7.2, '2026-03-29 09:15:00');

