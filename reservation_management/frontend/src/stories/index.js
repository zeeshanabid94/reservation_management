import React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';
import {Welcome } from '@storybook/react/demo';
import Calendar from '../components/calendar/calendar';
import App from '../App';
import { FormTextInput, FormButton } from '../components/input_elements/input_elements';
import { Modal } from '../components/modal/modal';

storiesOf('App', module)
    .add('App looks like', () => <App></App>)

storiesOf('Modal', module)
    .add('Modal Open', () => {
      let onChange = () => {
        console.log("Field changed");
      };
      let onSubmit = () => {
        console.log("Submitted");
      };
      let children = [
        <FormTextInput key='name' defaultValue='Enter your name here.' labelValue='Full Name' onChange={onChange}></FormTextInput>,
        <FormTextInput key='email' defaultValue='Enter your name here.' labelValue='Email' onChange={onChange}></FormTextInput>,
        <FormButton key='confirm' labelValue="Confirm" onSubmit={onSubmit}></FormButton>
        ]
      return <Modal show={true} children={children} heading="Reservation Confirmation"></Modal>
    }
    )
    .add('Modal Closed', () => {
      let onChange = () => {
        console.log("Field changed");
      };
      let onSubmit = () => {
        console.log("Submitted");
      };
      let children = [
        <FormTextInput key='name' defaultValue='Enter your name here.' labelValue='Full Name' onChange={onChange}></FormTextInput>,
        <FormTextInput key='email' defaultValue='Enter your name here.' labelValue='Email' onChange={onChange}></FormTextInput>,
        <FormButton key='confirm' labelValue="Confirm" onSubmit={onSubmit}></FormButton>
        ]
      return <Modal show={false} children={children} heading="Reservation Confirmation"></Modal>
    })

storiesOf('Input Elements', module)
    .add('Form Text Input', () => <FormTextInput key='name' defaultValue='Enter your name here.' labelValue='Full Name' onChange={
      () => console.log("On Change")
    }></FormTextInput>)
    .add('Button', () => <FormButton key='confirm' labelValue="Confirm" onSubmit={
      () => console.log("On Submit")
    }></FormButton> )
