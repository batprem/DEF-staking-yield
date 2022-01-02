import React from 'react';
import logo from './logo.svg';
import './App.css';
import { DAppProvider, ChainId, Chain, getChainById } from '@usedapp/core';
import { Header } from './components/Header';
import { Container } from "@material-ui/core";
import { Main } from './components/Main';
import { Kovan } from '@usedapp/core'


function App() {
  return (
    <DAppProvider config={{
      networks: [Kovan],
      notifications: {
        expirationPeriod: 1000,
        checkInterval: 1000 // Check transaction every 1 second
      }
    }}>
      < Header />
      <Container maxWidth="md">
        <div>
          Hi!
      </div>
        <Main />
      </Container>
    </DAppProvider>

  );
}

export default App;
