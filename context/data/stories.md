## fallback story
* out_of_scope
  - utter_out_of_scope

## welcome
* greet
  - utter_greet
  - utter_ask_name
> check_give_name

## give name
> check_give_name
* give_name
  - utter_personal_greeting
  - utter_ask_permission
> check_permission

## dont give name
> check_give_name
* deny OR deny_name
  - utter_no_worries
  - utter_ask_permission
> check_permission

## give permission and ask questions
> check_permission
* affirm
  - holiday_form
  - form{"name": "holiday_form"}
  - form{"name": null}
  - holiday_recommendation
  - utter_trial_close
> check_trial_close

## deny permission and ask question
> check_permission
* deny
  - utter_no_worries
  - utter_ask_experience
* request_holiday
  - holiday_recommendation
  - utter_trial_close
> check_trial_close

## trial close affirm loop
> check_trial_close
* affirm
  - utter_finish_recommendation
  - utter_continuation
* request_holiday

## trial close affirm goodbye
> check_trial_close
* affirm
  - utter_finish_recommendation
  - utter_continuation
* goodbye
  - utter_bye

## trial close deny
> check_trial_close
* deny
  - utter_try_again
  - action_reset_slots
  - holiday_form
  - form{"name": "holiday_form"}
  - form{"name": null}
  - holiday_recommendation
  - utter_trial_close
> check_trial_close

## trial close deny
> check_trial_close
* deny
  - utter_try_again
* deny
  - utter_no_worries
  - utter_bye

## say goodbye
* goodbye
  - utter_bye

## say thank you
* thanks
  - utter_accept_thanks

## invite bot
* invite bot
  - utter_accept_invitation

## New Story

* greet
    - utter_greet
    - utter_ask_name
* give_name{"user_name":"Joanne"}
    - slot{"user_name":"Joanne"}
    - slot{"user_name":"Joanne"}
    - utter_personal_greeting
    - utter_ask_permission
* affirm
    - holiday_form
    - form{"name":"holiday_form"}
    - slot{"requested_slot":"region"}
    - slot{"user_name":"Joanne"}
* request_holiday{"holiday_region":"zealand"}
    - holiday_form
    - slot{"region":"zealand"}
    - slot{"requested_slot":"season"}
* inform{"holiday_season":"jan-mar"}
    - holiday_form
    - slot{"season":"jan-mar"}
    - slot{"requested_slot":"budget"}
* inform{"holiday_budget":"mid-range"}
    - holiday_form
    - slot{"budget":"mid-range"}
    - slot{"requested_slot":"experience"}
* request_holiday{"holiday_experience":"adventure"}
    - holiday_form
    - slot{"experience":"adventure"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - holiday_recommendation
    - slot{"title":"Beach Break in Seminyak"}
    - slot{"description":"Seminyak is Bali's most sophisticated and upscale beach resort area, where the top draws are its beautiful beaches and sunsets"}
    - slot{"start_city":"Denpasar"}
    - slot{"region":"south east asia"}
    - slot{"season":"oct-dec"}
    - slot{"budget":"mid-range"}
    - slot{"country":"indonesia"}
    - slot{"experience":"relaxation"}
    - utter_trial_close
    - slot{"user_name":"Joanne"}
* deny
    - utter_try_again
    - action_reset_slots
    - slot{"title":null}
    - slot{"experience":null}
    - slot{"description":null}
    - slot{"start_city":null}
    - slot{"region":null}
    - slot{"season":null}
    - slot{"budget":null}
    - slot{"country":null}
    - utter_ask_experience
* request_holiday{"holiday_experience":"relaxation"}
    - slot{"user_name":"Joanne"}
    - holiday_recommendation
    - slot{"title":"Golden Triangle in India"}
    - slot{"description":"India's golden triangle is a tourist circuit which connects the national capital Delhi, Agra and Jaipur. ... The trips usually start in Delhi moving south to the site of Taj Mahal at Agra, then west, to the desert landscapes of Rajasthan."}
    - slot{"start_city":"Delhi"}
    - slot{"region":"asia"}
    - slot{"season":"oct-dec"}
    - slot{"budget":"mid-range"}
    - slot{"country":"india"}
    - slot{"experience":"culture"}
    - utter_trial_close
* inform
    - utter_finish_recommendation
    - utter_continuation
* goodbye
    - utter_bye
