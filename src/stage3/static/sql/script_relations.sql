--unicidad en tablas

ALTER TABLE bets.tb_teams
ADD CONSTRAINT constraint_unique_pk_teams UNIQUE (id_team);

ALTER TABLE bets.tb_scorers
ADD CONSTRAINT constraint_unique_pk_scorers UNIQUE (id);

ALTER TABLE bets.tb_positions
ADD CONSTRAINT constraint_unique_pk_positions UNIQUE (id);

--creación de relaciones

ALTER TABLE bets.tb_positions
ADD CONSTRAINT fk_tb_teams_id_team
FOREIGN KEY (id_team)
REFERENCES bets.tb_teams(id_team);

ALTER TABLE bets.tb_scorers
ADD CONSTRAINT fk_tb_scorers_id_team
FOREIGN KEY (id_team)
REFERENCES bets.tb_teams(id_team);


