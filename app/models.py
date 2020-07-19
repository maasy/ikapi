from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Users(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    cookie = fields.CharField(max_length=128)
    session_token = fields.CharField(max_length=256)
    created_at = DatetimeField()
    updated_at = DatetimeField()

class Battles(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    no = fields.IntField()
    game_mode = fields.CharField(max_length=20)
    rule = fields.CharField(max_length=20)
    type = fields.CharField(max_length=20)
    stage_id = fields.IntField()

    estimate_x_power = fields.IntField()
    estimate_gachi_power = fields.IntField()
    crown_players = fields.CharField(max_length=20)

    my_team_result = fields.CharField(max_length=20)
    other_team_result = fields.CharField(max_length=20)
    my_team_count = fields.IntField()
    other_team_count = fields.IntField()

    player_rank = fields.IntField()
    star_rank = fields.IntField()
    x_power = fields.FloatField()
    weapon_paint_point = fields.IntField()
    s_plus_number = fields.IntField()
    is_number_reached = fields.IntField()
    is_x = fields.IntField()
    number = fields.IntField()
    name = fields.CharField(max_length=20)

    start_time = fields.DatetimeField()
    elapsed_time = fields.IntField()


class Players(models.Model):
    id = fields.IntField(pk=True)
    battle_id = fields.IntField()

    nickname = fields.CharField(max_length=128)
    player_rank = fields.IntField()
    star_rank = fields.IntField()
    principal_id = fields.CharField(max_length=128)
    is_x = fields.IntField()
    udemae = fields.CharField(max_length=128)
    s_plus_number = fields.IntField()

    species = fields.CharField(max_length=128)
    style = fields.CharField(max_length=128)

    kill_count = fields.IntField()
    assist_count = fields.IntField()
    death_count = fields.IntField()
    special_count = fields.IntField()
    game_paint_point = fields.IntField()
    sort_score = fields.IntField()

    weapon_id = fields.IntField()
    head_gear_id = fields.IntField()
    clothes_gear_id = fields.IntField()
    shoes_gear_id = fields.IntField()
    head_main_skill_id = fields.IntField()
    head_sub_skill_1_id = fields.IntField()
    head_sub_skill_2_id = fields.IntField()
    head_sub_skill_3_id = fields.IntField()
    clothes_main_skill_id = fields.IntField()
    clothes_sub_skill_1_id = fields.IntField()
    clothes_sub_skill_2_id = fields.IntField()
    clothes_sub_skill_3_id = fields.IntField()
    shoes_main_skill_id = fields.IntField()
    shoes_sub_skill_1_id = fields.IntField()
    shoes_sub_skill_2_id = fields.IntField()
    shoes_sub_skill_3_id = fields.IntField()

Battle_Pydantic = pydantic_model_creator(Battles, name="Battle")
BattleIn_Pydantic = pydantic_model_creator(Battles,
                                         name="BattleIn",
                                         exclude_readonly=True)
